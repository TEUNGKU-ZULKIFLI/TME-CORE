#!/usr/bin/env python3
"""
Unit tests untuk AnomalyDetector (Jalur B)
Tests CPU baseline, spike detection, dan suspicious tracking

KEY INSIGHT:
AnomalyDetector uses suspicion_score accumulation:
- Each spike+success event adds 0.5 to score
- Threshold: score >= 0.7 → ANOMALY
- First event: score=0.5 → returns False
- Second event: score=1.0 → returns True ✅
"""

import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.detection.anomaly_detector import AnomalyDetector
from src.parser.log_parser import LoginEvent

def test_baseline_collection():
    """Test: Collect baseline CPU samples"""
    print("\n📊 test_baseline_collection...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    # Collect 10 samples at ~2% CPU (idle state)
    for i in range(10):
        detector.add_cpu_sample(2.0)
    
    # Verify baseline
    baseline = detector.get_baseline()
    assert baseline > 0, "Baseline should be > 0"
    assert 1.5 < baseline < 2.5, f"Baseline should be ~2%, got {baseline:.1f}%"
    
    print(f"  ✅ Baseline collected: {baseline:.1f}%")

def test_spike_detection():
    """
    Test: Detect anomaly when CPU spike + multiple successful logins
    
    KEY: Suspicion score requires 2+ events to reach threshold
    """
    print("\n📊 test_spike_detection...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    # Build baseline at 5% CPU
    for i in range(20):
        detector.add_cpu_sample(5.0)
    
    baseline = detector.get_baseline()
    print(f"  Baseline: {baseline:.1f}%")
    
    # Spike: +40% (5% + 40% = 7%)
    spike_cpu = baseline * 1.40  # 40% increase
    print(f"  Spike CPU: {spike_cpu:.1f}% (increase: 40%)")
    
    # EVENT 1: First successful login during spike
    event1 = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        username="admin",
        service="ssh",
        result="success"
    )
    
    result1 = detector.process_login_event(event1, current_cpu=spike_cpu)
    score1 = detector.suspicious_ips.get("192.168.1.100", 0)
    print(f"  Event 1: score={score1:.1f}, result={result1}")
    assert result1 == False, "First event should NOT trigger (score < 0.7)"
    
    # EVENT 2: Second successful login during spike (same IP)
    event2 = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        username="admin",
        service="ssh",
        result="success"
    )
    
    result2 = detector.process_login_event(event2, current_cpu=spike_cpu)
    score2 = detector.suspicious_ips.get("192.168.1.100", 0)
    print(f"  Event 2: score={score2:.1f}, result={result2}")
    assert result2 == True, f"Second event SHOULD trigger (score={score2:.1f} >= 0.7)"
    
    print(f"  ✅ Anomaly detection working (cumulative scoring)")

def test_cpu_insufficient_spike():
    """Test: Don't trigger if CPU spike < 30% threshold"""
    print("\n📊 test_cpu_insufficient_spike...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    # Build baseline at 10% CPU
    for i in range(20):
        detector.add_cpu_sample(10.0)
    
    baseline = detector.get_baseline()
    
    # Small spike: only +15% (need 30% threshold)
    spike_cpu = baseline * 1.15  # Only 15% increase
    
    event = LoginEvent(
        timestamp=datetime.now(),
        source_ip="192.168.1.101",
        username="admin",
        service="ssh",
        result="success"
    )
    
    result = detector.process_login_event(event, current_cpu=spike_cpu)
    score = detector.suspicious_ips.get("192.168.1.101", 0)
    
    print(f"  Current CPU: {spike_cpu:.1f}% (increase: 15%)")
    print(f"  Score: {score:.1f} (no spike → no score added)")
    assert result == False, "Should NOT trigger (spike < 30%)"
    assert score == 0, "Score should remain 0 (no spike detected)"
    
    print(f"  ✅ Correctly rejected insufficient spike")

def test_suspicious_score_accumulation():
    """Test: Suspicion score increases with repeated spike+success events"""
    print("\n📊 test_suspicious_score_accumulation...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    # Build baseline
    for i in range(10):
        detector.add_cpu_sample(8.0)
    
    baseline = detector.get_baseline()
    spike_cpu = baseline * 1.40
    
    scores = []
    
    # Simulate 3 consecutive spike+success events
    for attempt in range(1, 4):
        event = LoginEvent(
            timestamp=datetime.now(),
            source_ip="192.168.1.102",
            username="admin",
            service="ssh",
            result="success"
        )
        
        result = detector.process_login_event(event, current_cpu=spike_cpu)
        score = detector.suspicious_ips.get("192.168.1.102", 0)
        scores.append(score)
        
        print(f"  Attempt {attempt}: score={score:.1f}, anomaly={result}")
    
    # Verify score accumulates
    assert scores[0] == 0.5, f"First event: expected 0.5, got {scores[0]}"
    assert scores[1] == 1.0, f"Second event: expected 1.0, got {scores[1]}"
    assert scores[2] == 1.5, f"Third event: expected 1.5, got {scores[2]}"
    
    # Verify trigger happens on 2nd event
    assert True == detector.process_login_event(
        LoginEvent(
            timestamp=datetime.now(),
            source_ip="192.168.1.102",
            username="admin",
            service="ssh",
            result="success"
        ),
        current_cpu=spike_cpu
    ), "Should trigger after 2 events"
    
    print(f"  ✅ Score accumulation working correctly")

def test_multiple_ips_independent():
    """Test: Track multiple IPs independently"""
    print("\n📊 test_multiple_ips_independent...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    for i in range(10):
        detector.add_cpu_sample(5.0)
    
    baseline = detector.get_baseline()
    spike_cpu = baseline * 1.40
    
    # IP1: high spike
    for _ in range(2):
        detector.process_login_event(
            LoginEvent(
                timestamp=datetime.now(),
                source_ip="192.168.1.200",
                username="admin",
                service="ssh",
                result="success"
            ),
            current_cpu=spike_cpu
        )
    
    # IP2: normal CPU
    detector.process_login_event(
        LoginEvent(
            timestamp=datetime.now(),
            source_ip="192.168.1.201",
            username="admin",
            service="ssh",
            result="success"
        ),
        current_cpu=baseline * 0.9  # Below threshold
    )
    
    score1 = detector.suspicious_ips.get("192.168.1.200", 0)
    score2 = detector.suspicious_ips.get("192.168.1.201", 0)
    
    print(f"  IP 192.168.1.200 (spike): score={score1:.1f}")
    print(f"  IP 192.168.1.201 (normal): score={score2:.1f}")
    
    assert score1 >= 0.7, f"IP1 should have high score (got {score1})"
    assert score2 == 0, f"IP2 should have 0 score (got {score2})"
    
    print(f"  ✅ Multiple IPs tracked independently")

def test_reset_suspicious():
    """Test: Reset suspicion score for IP"""
    print("\n📊 test_reset_suspicious...")
    detector = AnomalyDetector(cpu_spike_threshold=30, window_seconds=60)
    
    for i in range(10):
        detector.add_cpu_sample(5.0)
    
    baseline = detector.get_baseline()
    spike_cpu = baseline * 1.40
    
    # Generate suspicious score
    for _ in range(2):
        detector.process_login_event(
            LoginEvent(
                timestamp=datetime.now(),
                source_ip="192.168.1.300",
                username="admin",
                service="ssh",
                result="success"
            ),
            current_cpu=spike_cpu
        )
    
    score_before = detector.suspicious_ips.get("192.168.1.300", 0)
    print(f"  Score before reset: {score_before:.1f}")
    
    # Reset
    detector.reset_suspicious("192.168.1.300")
    score_after = detector.suspicious_ips.get("192.168.1.300", 0)
    
    print(f"  Score after reset: {score_after:.1f}")
    assert score_after == 0, "Score should be 0 after reset"
    
    print(f"  ✅ Reset functionality working")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Running AnomalyDetector Unit Tests")
    print("=" * 60)
    
    try:
        test_baseline_collection()
        test_spike_detection()
        test_cpu_insufficient_spike()
        test_suspicious_score_accumulation()
        test_multiple_ips_independent()
        test_reset_suspicious()
        
        print("\n" + "=" * 60)
        print("✅ ALL ANOMALY DETECTOR TESTS PASSED")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
