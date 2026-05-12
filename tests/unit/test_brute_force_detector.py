#!/usr/bin/env python3
"""
Unit tests untuk BruteForceDetector (Jalur A)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.detection.brute_force_detector import BruteForceDetector
from src.parser.log_parser import LoginEvent

def test_threshold_detection():
    detector = BruteForceDetector(threshold=10, window_seconds=60)
    now = datetime.now()
    
    # Buat 9 failed attempts dalam window
    for i in range(9):
        event = LoginEvent(
            timestamp=now - timedelta(seconds=9-i),  # ✅ FIXED: 9s, 8s, ..., 1s lalu
            source_ip="192.168.1.100",
            username="admin",
            service="ssh",
            result="failure"
        )
        result = detector.process_event(event)
        assert result == False, f"Attempt {i+1} should not trigger"
    
    # Attempt ke-10 DALAM window yang sama (now)
    event_10 = LoginEvent(
        timestamp=now,  # ✅ Still within 60s window
        source_ip="192.168.1.100",
        username="admin",
        service="ssh",
        result="failure"
    )
    result = detector.process_event(event_10)
    assert result == True, "Should trigger at 10 attempts"  # ✅ NOW PASSES
    
    print("✅ test_threshold_detection PASSED")

def test_window_expiry():
    """Test: Events lama di-discard dari window"""
    detector = BruteForceDetector(threshold=5, window_seconds=60)
    
    now = datetime.now()
    
    # Add 3 events within window
    for i in range(3):
        event = LoginEvent(
            timestamp=now - timedelta(seconds=30),
            source_ip="192.168.1.100",
            username="admin",
            service="ssh",
            result="failure"
        )
        detector.process_event(event)
    
    # Add 2 old events (outside 60s window)
    for i in range(2):
        event = LoginEvent(
            timestamp=now - timedelta(seconds=120),  # 120 detik lalu
            source_ip="192.168.1.100",
            username="admin",
            service="ssh",
            result="failure"
        )
        detector.process_event(event)
    
    # Check current count (should be 3, not 5)
    count = detector.get_failed_count("192.168.1.100")
    assert count == 3, f"Expected 3 recent failures, got {count}"
    
    print("✅ test_window_expiry PASSED")

def test_multiple_ips():
    """Test: Separate tracking untuk each IP"""
    detector = BruteForceDetector(threshold=3, window_seconds=60)
    
    now = datetime.now()
    
    # 3 failures dari IP1
    for i in range(3):
        event = LoginEvent(
            timestamp=now - timedelta(seconds=i),
            source_ip="192.168.1.100",
            username="admin",
            service="ssh",
            result="failure"
        )
        result = detector.process_event(event)
        if i == 2:
            assert result == True, "IP1 should trigger at 3 failures"
    
    # 1 failure dari IP2 (should not trigger)
    event = LoginEvent(
        timestamp=now,
        source_ip="192.168.1.101",
        username="admin",
        service="ssh",
        result="failure"
    )
    assert detector.process_event(event) == False, "IP2 should not trigger with 1 failure"
    
    # Check counts
    assert detector.get_failed_count("192.168.1.100") == 3
    assert detector.get_failed_count("192.168.1.101") == 1
    
    print("✅ test_multiple_ips PASSED")

if __name__ == "__main__":
    print("🧪 Running BruteForceDetector Unit Tests...\n")
    test_threshold_detection()
    test_window_expiry()
    test_multiple_ips()
    print("\n✅ ALL TESTS PASSED")