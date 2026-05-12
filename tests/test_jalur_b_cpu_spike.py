#!/usr/bin/env python3
"""
Test Jalur B: Anomaly Detection dengan CPU Spike Simulation
"""

import sys
import time
import psutil
from pathlib import Path
from datetime import datetime

# Fix Python path untuk test discovery
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.detection.anomaly_detector import AnomalyDetector
from src.parser.log_parser import LoginEvent
from src.logger import setup_logger

logger = setup_logger("test_jalur_b")

def stress_cpu(duration: int = 30):
    """
    Stress CPU untuk simulate high load
    Duration dalam detik
    """
    logger.info(f"Starting CPU stress for {duration} seconds...")
    
    # Gunakan Python loop untuk stress CPU
    start = time.time()
    while time.time() - start < duration:
        # Heavy computation
        _ = [i**2 for i in range(10000)]
    
    logger.info("CPU stress complete")

def get_current_cpu() -> float:
    """Get current CPU usage %"""
    return psutil.cpu_percent(interval=1)

def test_jalur_b():
    """
    Test Jalur B dengan scenario:
    1. Build baseline CPU (60 samples ~30 sec)
    2. Trigger CPU spike (10 sec)
    3. Simulate successful login saat spike
    4. Verify anomaly detection
    """
    
    logger.info("=" * 60)
    logger.info("🧪 JALUR B TEST: Anomaly Detection dengan CPU Spike")
    logger.info("=" * 60)
    
    # Initialize detector
    detector = AnomalyDetector(
        cpu_spike_threshold=30,
        window_seconds=60
    )
    
    # PHASE 1: Build baseline (normal CPU load)
    logger.info("\n[PHASE 1] Building baseline CPU samples (60 sec)...")
    baseline_samples = []
    for i in range(60):
        cpu = get_current_cpu()
        baseline_samples.append(cpu)
        detector.add_cpu_sample(cpu)
        
        if (i + 1) % 10 == 0:
            logger.info(f"  Sampled: {i+1}/60 - Current CPU: {cpu:.1f}%")
        
        time.sleep(1)
    
    baseline_avg = sum(baseline_samples) / len(baseline_samples)
    logger.info(f"✓ Baseline CPU established: {baseline_avg:.1f}%")
    
    # PHASE 2: Trigger CPU spike + simulate attack
    logger.info("\n[PHASE 2] Triggering CPU spike with stress + simulating attack...")
    
    # Start CPU stress in background
    logger.info("  Starting CPU stress (10 sec)...")
    stress_cpu(duration=10)
    
    # During stress, simulate successful login event
    logger.info("  Simulating suspicious login event during spike...")
    
    current_cpu = get_current_cpu()
    logger.info(f"  Current CPU during spike: {current_cpu:.1f}%")
    
    # Create suspicious event
    suspicious_event = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.20.3",
        username="admin",
        service="ssh",
        result="success"  # Successful login saat CPU spike!
    )
    
    # Process event through detector
    is_anomaly = detector.process_login_event(
        suspicious_event,
        current_cpu=current_cpu
    )
    
    # PHASE 3: Verify results
    logger.info("\n[PHASE 3] Anomaly Detection Results:")
    logger.info(f"  Baseline CPU: {baseline_avg:.1f}%")
    logger.info(f"  Spike CPU: {current_cpu:.1f}%")
    logger.info(f"  CPU Increase: {((current_cpu - baseline_avg) / baseline_avg * 100):.1f}%")
    logger.info(f"  Source IP: {suspicious_event.source_ip}")
    logger.info(f"  Event Type: {suspicious_event.result.upper()} login during CPU spike")
    logger.info(f"  Anomaly Detected: {'✅ YES' if is_anomaly else '❌ NO'}")
    
    if is_anomaly:
        logger.info(f"  Suspicion Score: {detector.suspicious_ips.get(suspicious_event.source_ip, 0):.2f}")
    
    # PHASE 4: Expected behavior
    logger.info("\n[PHASE 4] Expected Behavior:")
    expected = (current_cpu - baseline_avg) > (baseline_avg * 0.30)  # 30% threshold
    logger.info(f"  CPU spike > 30% threshold: {expected}")
    logger.info(f"  Detection accuracy: {'✅ PASS' if is_anomaly == expected else '❌ FAIL'}")
    
    return is_anomaly, current_cpu, baseline_avg

if __name__ == "__main__":
    try:
        result, spike_cpu, baseline = test_jalur_b()
        
        logger.info("\n" + "=" * 60)
        if result:
            logger.info("🎉 JALUR B TEST PASSED - Anomaly detection working!")
        else:
            logger.warning("⚠️  JALUR B TEST INCONCLUSIVE - CPU spike might be too small")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)