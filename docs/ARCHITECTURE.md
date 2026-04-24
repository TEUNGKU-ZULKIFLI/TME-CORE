# Arsitektur Sistem TME-CORE

## 1. Topologi Lab Virtual

```
┌─────────────────────────────────────────────────────────────────┐
│                        NETWORK LAB ISOLATION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  KALI LINUX      │    │  DEBIAN SERVER   │                  │
│  │  (Attacker)      │◄──►│  (TME-CORE)      │                  │
│  │                  │    │                  │                  │
│  │ • Hydra/Medusa   │    │ • Python 3.11    │                  │
│  │ • Brute Force    │    │ • Engine         │                  │
│  │   Tools          │    │ • Log Parser     │                  │
│  │                  │    │ • Detectors      │                  │
│  └────────┬─────────┘    └─────────┬────────┘                  │
│           │                        │                            │
│           │ Attack (SSH/FTP)       │ API (port 8728)           │
│           │ (port 21, 22)          │                            │
│           │                        │                            │
│  ┌────────▼────────────────────────▼────────┐                  │
│  │     MIKROTIK ROUTEROS 6.49.19 (TARGET)   │                  │
│  │     hEX Board (RB750Gr2)                 │                  │
│  ├──────────────────────────────────────────┤                  │
│  │                                          │                  │
│  │  Interfaces:                             │                  │
│  │  ├─ ether1-ISP (Internet gateway)        │                  │
│  │  ├─ ether2 (192.168.10.1) ◄─ Debian     │                  │
│  │  ├─ ether3-5 (unused)                   │                  │
│  │                                          │                  │
│  │  Services:                               │                  │
│  │  ├─ SSH (port 22) ◄─ Kali brute force   │                  │
│  │  ├─ FTP (port 21) ◄─ Kali brute force   │                  │
│  │  ├─ API (port 8728) ◄─ Debian engine    │                  │
│  │  ├─ Firewall rules (address-list)       │                  │
│  │  └─ System resource (CPU/memory)        │                  │
│  │                                          │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

NETWORK DIAGRAM:

                    Kali Linux (192.168.x.x)
                           │
                           │ Brute Force Attack
                           │ SSH/FTP (port 21, 22)
                           ▼
    ┌─────────────────────────────────┐
    │   MikroTik RouterOS 6.49.19     │
    │   ether2: 192.168.10.1          │◄──────────┐
    │   API: 8728                     │           │
    │   SSH: 22                       │           │ API Commands
    │   FTP: 21                       │           │ (block_ip)
    └─────────────────────────────────┘           │
                                                  │
                                    Debian Server
                                    192.168.10.2
                                    (TME-CORE Engine)
```

## 2. Workflow Deteksi & Mitigasi

```
TIMELINE: Attack → Detection → Mitigation (Target: < 5 detik)

1. ATTACK INITIATION
   └─ Kali Linux: hydra -l admin -P wordlist.txt ssh://192.168.10.1
   └─ Result: Multiple failed login attempts

2. LOG GENERATION
   └─ MikroTik: Tulis ke /var/log/auth.log (SSH) atau /var/log/vsftpd.log (FTP)
   └─ Event: timestamp, username, src_ip, result (success/failure)

3. LOG PARSING (Debian)
   └─ Parser: Baca log real-time (tail mechanism)
   └─ Extract: LoginEvent(timestamp, src_ip, username, service, result)
   └─ Send to: Detectors

4. PARALLEL DETECTION (2 Jalur)
   
   ┌─ JALUR A: BRUTE FORCE DETECTION
   │  └─ Logic: Count failed attempts per IP (window 60 detik)
   │  └─ Trigger: count >= 10 → THREAT
   │  └─ Action: Signal "BLOCK_IP"
   │
   └─ JALUR B: ANOMALY DETECTION
      └─ Logic: Detect CPU spike saat login sukses
      └─ Baseline: Average CPU last 60 sec
      └─ Spike: CPU > baseline + 30%
      └─ Trigger: CPU_SPIKE + LOGIN_SUCCESS → SUSPICIOUS
      └─ Action: Signal "BLOCK_IP"

5. DECISION ENGINE
   └─ IF (Jalur_A_triggered OR Jalur_B_triggered) THEN:
      └─ Severity = HIGH
      └─ Action = BLOCK_IP (confidence: 95%)
      └─ Signal → Firewall Manager

6. FIREWALL ACTION
   └─ Call: MikroTik API (port 8728)
   └─ Command: /ip/firewall/address-list/add
   └─ Target: address=SOURCE_IP, list=brute_force_block
   └─ Effect: Firewall filter DROP incoming dari SOURCE_IP
   └─ Timing: < 5 detik dari trigger
   └─ Record: response_time, blocked_ip, timestamp

7. ALERTING
   └─ Send: Telegram Bot message
   └─ Content:
      🚨 THREAT DETECTED!
      ├─ Type: BRUTE_FORCE | ANOMALY
      ├─ Source IP: X.X.X.X
      ├─ Action: BLOCKED
      ├─ Response Time: 2.34 ms
      ├─ Router CPU: 45%
      └─ Timestamp: 2026-04-24T10:15:45

8. MONITORING
   └─ Metrics collected:
      ├─ response_time_ms (< 5000)
      ├─ router_cpu_percent (baseline vs spike)
      ├─ blocked_count (per attack session)
      ├─ false_positive_count (untuk validasi)
      └─ Save to: data/metrics/test_results.csv
```

## 3. Modul Core & Fungsi

| Modul | File | Fungsi | Input | Output |
|-------|------|--------|-------|--------|
| **Config Manager** | `src/config.py` | Load config dari .env + YAML | .env, app_config.yaml | Dict config |
| **Logger** | `src/logger.py` | Logging setup (file + console) | Log level, filename | Logger object |
| **Exception Handler** | `src/exceptions.py` | Custom exceptions | Error scenario | Exception class |
| **API Handler** | `src/api/mikrotik_client.py` | Koneksi RouterOS API, block/unblock | API credentials | Connection object |
| **Log Parser** | `src/parser/{ssh,ftp}_parser.py` | Parse SSH/FTP logs real-time | auth.log, vsftpd.log | LoginEvent stream |
| **BF Detector** | `src/detection/brute_force_detector.py` | Deteksi threshold failed login | LoginEvent | THREAT signal |
| **Anomaly Detector** | `src/detection/anomaly_detector.py` | Deteksi CPU spike + login correlation | LoginEvent, CPU metric | THREAT signal |
| **Firewall Manager** | `src/firewall/firewall_manager.py` | Orchestrate blocking & metrics | THREAT signal | API call, metrics |
| **Alert System** | `src/alert/telegram_alerter.py` | Send Telegram notifications | Alert data | Telegram message |
| **Metrics Collector** | `src/monitoring/metrics_collector.py` | Collect performance data | Event, timing, CPU | CSV/JSON data |
| **Main Engine** | `src/engine.py` | Orchestrate all modules | Config | Continuous monitoring |

## 4. Data Flow Diagram

```
User (Admin)
    │
    ▼
┌─────────────────────────────┐
│   Telegram Bot              │
│   Notifications             │◄───────┐
└─────────────────────────────┘        │
                                       │
                              ┌────────┴──────────┐
                              │ Alert System     │
                              │ telegram_alerter │
                              └────────┬──────────┘
                                       │
                              ┌────────▼──────────┐
                              │ Firewall Manager │
                              │ - block_ip()     │
                              │ - metrics        │
                              └────────┬──────────┘
                                       │
                              ┌────────▼──────────┐
                              │ Detection Engine │
                              │ ├─ Jalur A (BF) │
                              │ └─ Jalur B (CPU)│
                              └────────┬──────────┘
                                       │
                              ┌────────▼──────────┐
                              │ Log Parser       │
                              │ stream events    │
                              └────────┬──────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                     │
        ┌───────────▼────────┐            ┌──────────────▼────────┐
        │ /var/log/auth.log  │            │ /var/log/vsftpd.log  │
        │ (SSH)              │            │ (FTP)                │
        └────────────────────┘            └─────────────────────┘
                    ▲                                      ▲
                    │                                      │
        ┌───────────┴────────┐            ┌──────────────┴────────┐
        │ MikroTik SSH       │            │ MikroTik FTP        │
        │ Failed Login       │            │ Failed Login        │
        └────────────────────┘            └─────────────────────┘
                    ▲                                      ▲
                    │                                      │
        ┌───────────┴────────────────────────────────────┴────────┐
        │                                                          │
        │           Kali Linux (Hydra/Medusa Attack)              │
        │           Brute Force Attempts                          │
        │                                                          │
        └──────────────────────────────────────────────────────────┘
```

## 5. Deteksi vs Mitigasi: 2 Jalur Paralel

### **Jalur A: Brute Force Detection (Threshold-based)**
```
Input: LoginEvent (failed login)

Logic:
  failed_attempts[src_ip] = list of timestamps (failed logins)
  
  Current time: T
  Window: 60 detik (T-60 to T)
  
  Clean old entries:
    remove timestamps < (T - 60 seconds)
  
  Add current attempt:
    failed_attempts[src_ip].append(T)
    count = len(failed_attempts[src_ip])
  
  Check threshold:
    if count >= 10:
      return "THREAT_DETECTED"
    else:
      return None

Example:
  T=10:15:45, src_ip=192.168.1.50
  Attempts in window [10:14:45 - 10:15:45]:
    10:14:50, 10:14:52, 10:14:54, 10:14:56, 10:14:58,
    10:15:00, 10:15:02, 10:15:04, 10:15:06, 10:15:08, 10:15:45 (NEW)
    
  count = 11 >= 10
  → TRIGGER: Block 192.168.1.50
```

### **Jalur B: Anomaly Detection (CPU Correlation)**
```
Input: LoginEvent (successful login) + Router CPU

Logic:
  Baseline: Average CPU % last 60 sec
  
  Current event:
    - Type: Successful login
    - CPU now: 48%
    - Baseline CPU: 12%
    - Spike: (48 - 12) / 12 * 100 = 300% increase
  
  Check anomaly:
    if spike > 30%:  # 30% above baseline
      suspicion_score += 0.3
    
    if suspicion_score >= threshold (0.7):
      return "ANOMALY_DETECTED"

Example:
  Normal login success: CPU 12%, suspicion_score = 0 → PASS
  
  Login during CPU spike: CPU 48%, spike=300%
    → suspicion_score = 0.3 + 0.3 + 0.3 = 0.9 >= 0.7
    → TRIGGER: Block source_ip
```

## 6. Konfigurasi Threshold & Parameter

**File:** `config/app_config.yaml`

```yaml
detection:
  brute_force:
    threshold: 10              # >= 10 failed attempts
    window_seconds: 60         # dalam 60 detik
    action: BLOCK              # Aksi jika triggered
  
  anomaly:
    cpu_spike_threshold: 30    # 30% above baseline
    window_seconds: 60
    suspicious_score_threshold: 0.7
    action: BLOCK

mitigasi:
  max_response_time_ms: 5000   # Target: < 5 detik
  auto_unblock_minutes: 60     # Auto unblock setelah 60 menit (optional)
  address_list: brute_force_block
```

## 7. Success Criteria (Target)

| Metric | Target | Status |
|--------|--------|--------|
| Deteksi Brute Force | < 5 detik | ⏳ Testing |
| Response Time Mitigasi | < 5 detik | ⏳ Testing |
| Router CPU Impact | < 50% | ⏳ Testing |
| False Positive Rate | < 5% | ⏳ Testing |
| Alert Delivery | 100% to Telegram | ⏳ Testing |
| Uptime Engine | > 99% | ⏳ Testing |

---

## Referensi

- MikroTik API Documentation: https://wiki.mikrotik.com/wiki/Manual:API
- RouterOS Log Format: https://wiki.mikrotik.com/wiki/Manual:System/Log
- Python routeros-api: https://github.com/socialwifi/RouterOS-api-python