# Threat Analysis: Brute Force Attacks pada SSH & FTP

## 1. Attack Vector

### SSH Brute Force
- **Port**: 22
- **Target**: /var/log/auth.log
- **Pattern**: Failed password attempts
- **Typical behavior**: 10+ attempts dalam 60 detik

### FTP Brute Force
- **Port**: 21
- **Target**: /var/log/vsftpd.log
- **Pattern**: LOGIN FAILED events
- **Typical behavior**: 8+ attempts dalam 60 detik

## 2. Log Parsing Patterns

### SSH Failed Login (auth.log)
```regex
Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)
```

### FTP Failed Login (vsftpd.log)
```regex
(\d+\.\d+\.\d+\.\d+).*LOGIN FAILED
```

## 3. Detection Thresholds

| Parameter | Value | Justification |
|-----------|-------|---------------|
| BF_THRESHOLD | 10 attempts | Standard fail-count untuk brute force |
| BF_WINDOW | 60 seconds | Time window untuk aggregation |
| CPU_SPIKE | 30% above baseline | Significant anomaly indicator |
| RESPONSE_TIME | <5 seconds | Target mitigasi latency |

## 4. Baseline Metrics (To be collected)

- Normal CPU: [akan diisi setelah collection]
- Normal Memory: [akan diisi setelah collection]
- Normal Network I/O: [akan diisi setelah collection]

## 5. Real Attack Testing Results

### Test Scenario
- **Date**: 2026-05-09
- **Attack Tool**: Hydra v9.6
- **Target**: SSH 192.168.20.1:22
- **Attacker**: Kali Linux 192.168.20.2
- **Duration**: ~9 minutes

### Real Attack Metrics
```
Failed Login Attempts: 21+ in first 60 seconds
Event Rate: ~7 events/second
Log Format: ISO8601 timestamp + severity level

Sample Events:
2026-05-09T08:00:04.680892-07:00 192.168.10.1 system,error,critical login failure for user admin from 192.168.20.2 via ssh
2026-05-09T08:00:04.708107-07:00 192.168.10.1 system,error,critical login failure for user admin from 192.168.20.2 via ssh
2026-05-09T08:00:04.733870-07:00 192.168.10.1 system,error,critical login failure for user admin from 192.168.20.2 via ssh
```

### Engine Performance
- **Config Loading Time**: <100ms
- **API Connection Time**: <500ms
- **Log Parser Startup**: <200ms
- **Brute Force Detection Threshold**: 10 failures
- **Detection Accuracy**: 100% (correct IP identification)
- **Blocking Response Time**: 7.03ms ✅ (Target: <5000ms)
- **Mitigation Action**: Automatic IP add to address-list:brute_force_block

### Results
✅ Attacker IP (192.168.20.2) successfully blocked after 10th failed attempt
✅ Firewall DROP rule applied real-time
✅ Ping from attacker: 0% success rate (100% packet loss)
✅ Metrics saved to engine_metrics.csv (1 blocking event recorded)
✅ No false positives observed
✅ Engine maintained stable operation during 9-minute attack

### Conclusion
Engine successfully detected and mitigated brute force attack in real-time with <10ms response time.