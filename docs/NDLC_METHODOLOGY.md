# NDLC (Network Development Life Cycle) Methodology

## Pengenalan NDLC

NDLC adalah metodologi sistematis untuk pengembangan, implementasi, dan evaluasi solusi networking. Cocok untuk penelitian akademik karena memberikan struktur terukur dan dokumentasi komprehensif di setiap fase.

**Fase NDLC:**
1. **Initiation** - Perencanaan & persiapan awal
2. **Analysis** - Analisis kebutuhan & baseline
3. **Design** - Perancangan solusi
4. **Implementation** - Implementasi & pengkodean
5. **Testing/Evaluation** - Pengujian & validasi
6. **Deployment** - Rilis & dokumentasi final

---

## Fase 1: INITIATION (Apr 24-25)

### Tujuan
Mempersiapkan infrastruktur lab, mendokumentasikan requirements, dan setup project management.

### Deliverables
- ✅ Lab virtual siap (Debian, MikroTik, Kali Linux)
- ✅ Repository dengan struktur clean
- ✅ GitHub Issues & Milestones
- ✅ Dokumentasi awal (ARCHITECTURE, SETUP_LAB, NDLC_METHODOLOGY)

### Checklist
- [x] Branch refactor/ndlc-structure dibuat
- [x] Folder structure setup
- [x] Dependencies terinstall
- [x] 8 GitHub Issues created
- [ ] **CURRENT**: Dokumentasi dasar
- [ ] Sample logs uploaded
- [ ] API connection tested

---

## Fase 2: ANALYSIS (Apr 26-27)

### Tujuan
Analisis mendalam: attack patterns, baseline metrics, threshold determination.

### Deliverables
- THREAT_ANALYSIS.md (attack vectors & patterns)
- Baseline metrics CSV (60 samples CPU/memory/network)
- Regex pattern definitions (SSH & FTP)
- Threshold justification document

### Tasks
1. Study brute force attack behavior
   - SSH attack patterns (auth.log)
   - FTP attack patterns (vsftpd.log)
   - Timing & frequency characteristics

2. Collect baseline metrics
   - Router CPU usage (normal operation)
   - Memory consumption
   - Network throughput
   - Collect ≥60 samples over 1 hour

3. Define detection thresholds
   - BF_THRESHOLD: >= 10 failed attempts
   - BF_WINDOW: 60 seconds
   - CPU_SPIKE_THRESHOLD: > 30% above baseline
   - Response time target: < 5 seconds

4. Analysis & validation
   - Compare dengan similar research
   - Document justification
   - Create metrics baseline CSV

---

## Fase 3: DESIGN (Apr 28-29)

### Tujuan
Perancangan detail arsitektur, modul, API protocol, database schema.

### Deliverables
- DESIGN_DOCUMENT.md (complete)
- UML class diagram (6 modules)
- Sequence diagram (blocking flow)
- Database schema (SQLite ERD)
- API communication protocol
- Error handling matrix

### Tasks
1. Modul design
   - Config Manager
   - Logger
   - Exception Handler
   - API Handler
   - Log Parser (SSH + FTP)
   - Brute Force Detector
   - Anomaly Detector
   - Firewall Manager
   - Alert System
   - Metrics Collector
   - Main Engine

2. API protocol design
   - MikroTik API command mapping
   - Blocking sequence
   - Error recovery strategy

3. Database schema
   - events table (login records)
   - blocks table (IP blocks)
   - metrics table (performance data)

4. Alert format
   - Telegram message structure
   - Alert content & severity levels

---

## Fase 4: IMPLEMENTATION (Apr 30 - May 11)

### Tujuan
Implementasi modular: dari API layer hingga orchestrator, dengan unit testing.

### Deliverables
- **Sprint A** (Apr 30-May 2): API layer complete + unit tests
  - `src/api/mikrotik_client.py`
  - `src/config.py`, `src/logger.py`, `src/exceptions.py`
  - `tests/unit/test_api.py`

- **Sprint B** (May 3-5): Log Parser complete + unit tests
  - `src/parser/` (base, SSH, FTP)
  - `tests/unit/test_parser.py`
  - Sample logs in `data/samples/`

- **Sprint C** (May 6-11): Detectors + Integration + Main Engine
  - `src/detection/` (BF detector, Anomaly detector)
  - `src/firewall/firewall_manager.py`
  - `src/alert/telegram_alerter.py`
  - `src/monitoring/metrics_collector.py`
  - `src/engine.py` (main orchestrator)
  - `tests/` (unit + integration tests)

### Tasks per Sprint

**Sprint A: API Layer**
```
- [ ] src/config.py: Config loading (env + YAML)
- [ ] src/logger.py: Logging setup (rotating file handler)
- [ ] src/exceptions.py: Custom exceptions (6 types)
- [ ] src/api/mikrotik_client.py:
      - __init__(host, username, password, port, timeout)
      - connect() / disconnect()
      - execute_command(path, arguments)
      - block_ip(ip) / unblock_ip(ip)
      - get_router_cpu() / list_address_lists()
- [ ] tests/unit/test_api.py:
      - test_connect_success
      - test_block_ip_success
      - test_unblock_ip_success
      - test_connection_retry
      - test_error_handling
- [ ] All unit tests passing (pytest)
- [ ] PR & merge to refactor/ndlc-structure
```

**Sprint B: Log Parser**
```
- [ ] src/parser/models.py: LoginEvent dataclass
- [ ] src/parser/log_parser.py: Base parser + streaming
- [ ] src/parser/ssh_parser.py: SSH-specific parsing
- [ ] src/parser/ftp_parser.py: FTP-specific parsing
- [ ] tests/unit/test_parser.py:
      - test_parse_ssh_failure
      - test_parse_ftp_failure
      - test_streaming_mechanism
      - test_event_extraction
- [ ] data/samples/auth.log: Sample SSH log
- [ ] data/samples/vsftpd.log: Sample FTP log
- [ ] All unit tests passing
- [ ] PR & merge
```

**Sprint C: Detection & Integration**
```
- [ ] src/detection/base_detector.py: Abstract base
- [ ] src/detection/brute_force_detector.py:
      - threshold-based detection
      - sliding window logic
- [ ] src/detection/anomaly_detector.py:
      - CPU monitoring & correlation
      - suspicion scoring
- [ ] src/firewall/firewall_manager.py:
      - orchestrate blocking
      - record response times & metrics
- [ ] src/alert/telegram_alerter.py:
      - send formatted alerts
      - handle bot token & chat ID
- [ ] src/monitoring/metrics_collector.py:
      - collect performance data
      - save to CSV/JSON
- [ ] src/engine.py:
      - main loop
      - module orchestration
      - error handling & recovery
- [ ] tests/unit/ & tests/integration/:
      - 30+ unit tests
      - 5+ integration tests
- [ ] All tests passing (90%+ coverage on core)
- [ ] PR & merge
```

---

## Fase 5: TESTING & EVALUATION (May 12-14)

### Tujuan
Pengujian lapangan dengan attack scenario real, collect metrics, validate effectiveness.

### Deliverables
- TEST_PROTOCOL.md (testing procedure)
- test_results.csv (metrics from attack scenarios)
- TEST_REPORT.md (analysis & findings)
- Success/failure justification

### Testing Scenarios

**Scenario 1: SSH Brute Force Attack**
```
Setup:
  - Kali Linux siap dengan Hydra
  - MikroTik dengan clean address-list
  - TME-CORE engine running
  - Monitoring: logs, CPU, Telegram alerts

Attack:
  hydra -l admin -P wordlist.txt ssh://192.168.10.1 -o /tmp/hydra-ssh.txt

Monitoring:
  - Terminal 1: tail -f data/logs/tme_core.log
  - Terminal 2: Watch MikroTik CPU (API polling)
  - Terminal 3: Monitor Telegram alerts

Collect metrics:
  - timestamp (attack start)
  - event_type: BRUTE_FORCE
  - source_ip: Kali IP
  - detection_time: ms from first event to detection
  - mitigation_time: ms from detection to block
  - router_cpu: before, during, after attack
  - blocked_count: number of IPs blocked
  - alert_sent: yes/no
  - false_positive: yes/no

Save to: data/metrics/ssh_brute_force_test.csv
```

**Scenario 2: FTP Brute Force Attack**
```
Similar ke SSH, tapi gunakan FTP:
  hydra -l admin -P wordlist.txt ftp://192.168.10.1
```

**Scenario 3: Mixed Attack (SSH + FTP Parallel)**
```
Run SSH & FTP attack simultaneously, measure resource contention
```

### Metrics Collection

**CSV Format:**
```
timestamp,source_ip,service,event_type,detection_time_ms,mitigation_time_ms,action,router_cpu_before,router_cpu_after,failed_count,alert_sent,false_positive
2026-05-12T10:15:45Z,192.168.1.50,ssh,brute_force,1200,2340,BLOCK,12,42,47,yes,no
2026-05-12T10:16:30Z,192.168.1.51,ftp,brute_force,980,1850,BLOCK,15,44,38,yes,no
```

### Success Criteria

| Metric | Target | Pass/Fail |
|--------|--------|-----------|
| Detection Time | < 2 detik | ? |
| Mitigation Time | < 5 detik | ? |
| CPU Impact | < 50% | ? |
| False Positive Rate | < 5% | ? |
| Alert Delivery | 100% | ? |
| Router Stability | No crash | ? |

---

## Fase 6: DEPLOYMENT & RELEASE (May 15-21)

### Tujuan
Finalisasi kode, dokumentasi lengkap, release V1.0.0, penulisan skripsi.

### Deliverables
- Clean, production-ready code
- Complete API documentation
- Installation guide
- Skripsi complete (7 chapters + appendix)
- GitHub release v1.0.0
- Dataset & analysis

### Tasks

**Code Finalization:**
- [ ] Code review (PEP8, docstring, type hints)
- [ ] All tests passing (100%)
- [ ] No warnings/deprecations
- [ ] Documentation strings lengkap

**Documentation:**
- [ ] API documentation (Sphinx/MkDocs)
- [ ] README.md update
- [ ] CONTRIBUTING.md
- [ ] INSTALLATION.md
- [ ] TROUBLESHOOTING.md

**Thesis Writing:**
- [ ] BAB I: Pendahuluan (problem, objective, scope)
- [ ] BAB II: Tinjauan Pustaka (related work, theoretical background)
- [ ] BAB III: Metodologi (NDLC phases, research design)
- [ ] BAB IV: Implementasi (architecture, code walkthrough)
- [ ] BAB V: Hasil & Analisis (metrics, charts, statistical analysis)
- [ ] BAB VI: Diskusi (findings interpretation, limitations)
- [ ] BAB VII: Kesimpulan & Saran (summary, future work)
- [ ] LAMPIRAN A: Source code
- [ ] LAMPIRAN B: Test results dataset
- [ ] LAMPIRAN C: Topology diagrams

**Release:**
- [ ] Git tag v1.0.0
- [ ] GitHub Release page created
- [ ] Upload dataset (CSV + charts)
- [ ] Announce in README

---

## Summary: NDLC Timeline

```
TIMELINE VISUAL:

Apr 24-25  | Initiation  | ✅ ➜ Branch, docs, issues
Apr 26-27  | Analysis    | ⏳ ➜ Attack analysis, baseline metrics
Apr 28-29  | Design      | ⏳ ➜ UML, schema, protocol
Apr 30-    | Implementation
           | Sprint A    | ⏳ ➜ API layer
           | Sprint B    | ⏳ ➜ Log parser
May 6-11   | Sprint C    | ⏳ ➜ Detectors + integration
May 12-14  | Testing     | ⏳ ➜ Hydra/Medusa attacks, metrics
May 15-21  | Deployment  | ⏳ ➜ Code finalization, thesis, release v1.0.0

Total: 4 minggu → V1.0.0 Ready! 🎉
```

---

## Benefits of NDLC untuk Skripsi

1. **Struktur sistematis** → Mudah tracking progress & explain ke dosen
2. **Evidence-based** → Setiap fase punya deliverable & dokumentasi
3. **Measurable outcomes** → Metrics & data collection terstruktur
4. **Reproducible** → Lab setup & testing bisa direplikasi
5. **Professional approach** → Sesuai standar networking research
