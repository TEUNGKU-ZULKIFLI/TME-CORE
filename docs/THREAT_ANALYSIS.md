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
