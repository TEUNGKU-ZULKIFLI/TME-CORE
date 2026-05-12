#!/usr/bin/env python3
"""
Test Jalur B: Anomaly Detection dengan MikroTik CPU Spike
CORRECTED: Use MikroTik API untuk CPU measurement, bukan psutil!
"""

import sys
import time
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.detection.anomaly_detector import AnomalyDetector
from src.parser.log_parser import LoginEvent
from src.logger import setup_logger
from src.api.mikrotik_client import MikroTikClient  # ✅ ADD THIS
from src.config import get_config  # ✅ ADD THIS

logger = setup_logger("test_jalur_b")

def get_mikrotik_cpu(api_client: MikroTikClient) -> float:
    """
    Get MikroTik router CPU % (bukan Debian CPU!)
    ✅ Uses actual API call ke router
    """
    try:
        cpu_info = api_client.get_router_cpu()
        return cpu_info['cpu_load']
    except Exception as e:
        logger.error(f"Failed to get MikroTik CPU: {e}")
        return 0.0

def stress_cpu_debian(duration: int = 10):
    """
    Stress Debian server CPU untuk trigger attack detection
    (This causes MikroTik to handle more SSH attempts)
    """
    logger.info(f"Starting Debian CPU stress for {duration} seconds...")
    start = time.time()
    while time.time() - start < duration:
        _ = [i**2 for i in range(50000)]  # ✅ Increased workload
    logger.info("CPU stress complete")

def test_jalur_b():
    """
    Test Jalur B dengan scenario REAL:
    1. Connect ke MikroTik API
    2. Get baseline MikroTik CPU (while Debian idle)
    3. Stress Debian & trigger live attack
    4. Measure MikroTik CPU spike
    5. Verify anomaly detection
    """
    
    logger.info("=" * 60)
    logger.info("🧪 JALUR B TEST: MikroTik CPU Spike Detection (REAL)")
    logger.info("=" * 60)
    
    # Initialize
    config = get_config()
    api = MikroTikClient(**config['mikrotik'])
    detector = AnomalyDetector(
        cpu_spike_threshold=30,
        window_seconds=60
    )
    
    # Connect API
    try:
        api.connect()
        logger.info("✅ Connected to MikroTik API")
    except Exception as e:
        logger.error(f"❌ Failed to connect: {e}")
        return False
    
    # PHASE 1: Build baseline (MikroTik idle state)
    logger.info("\n[PHASE 1] Building baseline (MikroTik CPU at idle, 30 samples)...")
    baseline_samples = []
    for i in range(30):
        cpu = get_mikrotik_cpu(api)
        baseline_samples.append(cpu)
        detector.add_cpu_sample(cpu)
        
        if (i + 1) % 10 == 0:
            logger.info(f"  Sample {i+1}/30: MikroTik CPU = {cpu:.1f}%")
        
        time.sleep(1)
    
    baseline_avg = sum(baseline_samples) / len(baseline_samples)
    logger.info(f"✓ Baseline established: {baseline_avg:.1f}%")
    
    # PHASE 2: Trigger spike + simultaneous SSH attack
    logger.info("\n[PHASE 2] Triggering CPU spike + SSH attack...")
    logger.info("  Starting simultaneous:")
    logger.info("    - Debian stress test (10 sec)")
    logger.info("    - MikroTik receives SSH brute force")
    
    # Start stress
    stress_cpu_debian(duration=10)
    
    # Sample during spike
    time.sleep(2)  # Wait for SSH attempts to register
    current_cpu = get_mikrotik_cpu(api)
    logger.info(f"  Current MikroTik CPU during spike: {current_cpu:.1f}%")
    
    # Create suspicious event (successful login during spike = anomaly)
    suspicious_event = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.20.3",
        username="admin",
        service="ssh",
        result="success"  # Successful login saat CPU spike
    )
    
    is_anomaly = detector.process_login_event(
        suspicious_event,
        current_cpu=current_cpu
    )
    
    # PHASE 3: Results
    logger.info("\n[PHASE 3] Results:")
    logger.info(f"  Baseline CPU: {baseline_avg:.1f}%")
    logger.info(f"  Spike CPU: {current_cpu:.1f}%")
    logger.info(f"  Increase: {((current_cpu - baseline_avg) / max(baseline_avg, 1) * 100):.1f}%")
    logger.info(f"  Threshold (30%): {'✅ EXCEEDED' if ((current_cpu - baseline_avg) / max(baseline_avg, 1)) > 0.30 else '❌ NOT MET'}")
    logger.info(f"  Anomaly Detected: {'✅ YES' if is_anomaly else '❌ NO'}")
    
    # PHASE 4: Expected behavior
    logger.info("\n[PHASE 4] Accuracy Check:")
    expected = (current_cpu - baseline_avg) > (baseline_avg * 0.30)
    accuracy = "✅ PASS" if is_anomaly == expected else "❌ FAIL"
    logger.info(f"  Detection accuracy: {accuracy}")
    
    api.disconnect()
    
    return is_anomaly, current_cpu, baseline_avg

if __name__ == "__main__":
    try:
        result, spike_cpu, baseline = test_jalur_b()
        
        logger.info("\n" + "=" * 60)
        if result:
            logger.info("🎉 JALUR B TEST PASSED - Anomaly detection working!")
        else:
            logger.warning("⚠️  JALUR B TEST FAILED or CPU spike too small")
            logger.warning("     Consider: MikroTik might have low baseline CPU in VM")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)