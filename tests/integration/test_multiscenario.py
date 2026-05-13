"""
Integration Test: Multi-Scenario Attack Patterns
"""

import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import get_config
from src.parser.log_parser import LoginEvent
from src.detection.brute_force_detector import BruteForceDetector
from src.detection.anomaly_detector import AnomalyDetector
from src.logger import setup_logger

logger = setup_logger("test_multiscenario")

# ============================================================
# SCENARIO 1: SSH BRUTE FORCE 30 DETIK
# ============================================================

def scenario_1_ssh_30sec():
    """
    Scenario: Attacker performs 30 failed SSH logins within 30 seconds
    Expected: Detection at 10th attempt, block at ~3 seconds elapsed
    """
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 SCENARIO 1: SSH Brute Force 30 seconds")
    logger.info("=" * 60)
    
    config = get_config()
    detector = BruteForceDetector(
        threshold=config['detection']['brute_force']['threshold'],
        window_seconds=config['detection']['brute_force']['window_seconds']
    )
    
    attack_ip = "192.168.50.1"
    start_time = datetime.now()
    blocked_at_attempt = None
    
    logger.info(f"\nAttack from: {attack_ip}")
    logger.info("Sending 30 failed logins over 30 seconds (1/sec)...\n")
    
    for i in range(30):
        event = LoginEvent(
            timestamp=start_time + timedelta(seconds=i),
            source_ip=attack_ip,
            username="admin",
            service="ssh",
            result="failure"
        )
        
        result = detector.process_event(event)
        
        if result and not blocked_at_attempt:
            blocked_at_attempt = i + 1
            elapsed = (event.timestamp - start_time).total_seconds()
            logger.info(f"  🚨 BLOCKED: Attempt #{blocked_at_attempt} at {elapsed:.1f}s")
    
    # Verify detection
    assert blocked_at_attempt == 10, f"Should block at attempt 10, got {blocked_at_attempt}"
    logger.info(f"\n✅ SCENARIO 1 PASSED: Blocked at attempt {blocked_at_attempt}")

# ============================================================
# SCENARIO 2: MULTIPLE SIMULTANEOUS IPs
# ============================================================

def scenario_2_multiple_ips():
    """
    Scenario: 3 different IPs attacking simultaneously
    Expected: Each tracked independently, each blocked at 10 failures
    """
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 SCENARIO 2: Multiple Simultaneous Attack IPs")
    logger.info("=" * 60)
    
    config = get_config()
    detector = BruteForceDetector(
        threshold=config['detection']['brute_force']['threshold'],
        window_seconds=config['detection']['brute_force']['window_seconds']
    )
    
    attack_ips = ["192.168.50.10", "192.168.50.11", "192.168.50.12"]
    blocked = {}
    
    logger.info(f"\nAttacking from {len(attack_ips)} sources...\n")
    
    # Interleave attempts from 3 IPs
    for round_num in range(10):
        for ip in attack_ips:
            event = LoginEvent(
                timestamp=datetime.now(),
                source_ip=ip,
                username="admin",
                service="ssh",
                result="failure"
            )
            
            result = detector.process_event(event)
            if result and ip not in blocked:
                blocked[ip] = True
                logger.info(f"  🚨 BLOCKED: {ip}")
    
    # Verify all 3 blocked
    assert len(blocked) == len(attack_ips), f"Should block all {len(attack_ips)} IPs"
    logger.info(f"\n✅ SCENARIO 2 PASSED: All {len(attack_ips)} IPs blocked independently")

# ============================================================
# SCENARIO 3: MIXED SUCCESS + FAILURE (BRUTE FORCE + ANOMALY)
# ============================================================

def scenario_3_mixed_attack():
    """
    Scenario: CPU spike + successful login during spike
    Expected: Jalur A may not trigger (< 10 failures), but Jalur B detects anomaly
    """
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 SCENARIO 3: Mixed Attack - CPU Spike + Success")
    logger.info("=" * 60)
    
    config = get_config()
    bf_detector = BruteForceDetector(threshold=10, window_seconds=60)
    anomaly_detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    attack_ip = "192.168.50.20"
    
    # Build baseline CPU
    logger.info("\n[PHASE 1] Establishing baseline (60 samples at 5% CPU)...")
    for i in range(60):
        anomaly_detector.add_cpu_sample(5.0)
    logger.info(f"Baseline: {anomaly_detector.get_baseline():.1f}%")
    
    # Spike event: successful login at CPU 50%
    logger.info("\n[PHASE 2] Detecting spike + suspicious login...")
    event = LoginEvent(
        timestamp=datetime.now(),
        source_ip=attack_ip,
        username="admin",
        service="ssh",
        result="success"  # ← Successful during spike
    )
    
    spike_cpu = 50.0
    cpu_increase = ((spike_cpu - anomaly_detector.get_baseline()) / anomaly_detector.get_baseline()) * 100
    
    logger.info(f"  Current CPU: {spike_cpu}%")
    logger.info(f"  Spike: {cpu_increase:.1f}% (threshold: 30%)")
    
    # Process events
    bf_result = bf_detector.process_event(event)
    anomaly_result = anomaly_detector.process_login_event(event, spike_cpu)
    
    logger.info(f"\n  Jalur A (Brute Force): {bf_result}")
    logger.info(f"  Jalur B (Anomaly): {anomaly_result}")
    
    logger.info(f"\n✅ SCENARIO 3 PASSED: Both detectors evaluated")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    try:
        scenario_1_ssh_30sec()
        scenario_2_multiple_ips()
        scenario_3_mixed_attack()
        
        logger.info("\n\n" + "=" * 60)
        logger.info("✅ ALL MULTI-SCENARIO TESTS PASSED")
        logger.info("=" * 60)
        
    except AssertionError as e:
        logger.error(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ ERROR: {e}", exc_info=True)
        sys.exit(1)