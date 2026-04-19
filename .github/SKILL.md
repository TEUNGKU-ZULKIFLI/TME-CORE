# 🤖 AI Assistant Skill Description

**Dokumen ini untuk Vibes Coders: Programmer yang bekerja dengan AI Assistant**

Gunakan file ini untuk mengoptimalkan performa AI Assistant dalam project TME-CORE.

---

## 📋 PROJECT CONTEXT

### Project Overview
- **Nama**: TME-CORE (Traffic Mitigation External Core)
- **Tujuan**: Sistem keamanan otonom untuk melindungi MikroTik router dari brute force attacks
- **Tech Stack**: Python 3.12+, MikroTik API, Telegram Bot API
- **Framework**: NDLC (Network Development Life Cycle) - 6 phases
- **Language**: Bahasa Indonesia sebagai bahasa utama komunikasi
- **Developer Role**: Vibes Coder (memanfaatkan AI Assistant)

### Architecture Overview
```
MikroTik Router
    ↓ API (port 8728)
Debian Server (Python Engine)
    ├─ Log Parser
    ├─ Threat Detector
    ├─ Firewall Manager
    └─ Alert System
         ↓ HTTPS
    Telegram Bot
```

---

## 🎯 CORE FEATURES TO IMPLEMENT

### Phase 1: ANALYSIS (Issue #2)
**Goals**: Define requirements, threat model, metrics
- [ ] Document threat scenarios
- [ ] Define detection thresholds
- [ ] Performance metrics baseline
- [ ] API capability assessment

**AI Assistant Skills Needed**:
- Threat modeling & analysis
- Security requirements definition
- Metrics & KPI definition
- Documentation writing

**Prompt Examples**:
```
"Analisa threat scenarios untuk brute force SSH dan FTP. Apa saja attack patterns yang harus dideteksi?"

"Define detection threshold untuk brute force. Berapa attempts per minute yang reasonable untuk false positive minimized?"

"Buat security requirement document untuk sistem mitigasi ini."
```

---

### Phase 2: DESIGN (Issue #3)
**Goals**: System architecture, API specs, design docs
- [ ] Architecture diagram (ASCII/Mermaid)
- [ ] API specification document
- [ ] Module design & interfaces
- [ ] Database schema (jika diperlukan)
- [ ] Flow diagrams

**AI Assistant Skills Needed**:
- System design & architecture
- API design best practices
- UML/diagram generation
- Technical documentation

**Prompt Examples**:
```
"Design modul structure untuk TME-CORE. Pisahkan concerns antara: API connection, log parsing, detection, firewall, alerting"

"Buat sequence diagram untuk threat detection flow (dari log acquisition sampai firewall block)"

"Spec-kan interface untuk MikroTik API client. Apa methods yang diperlukan?"
```

---

### Phase 3: SIMULATION (Issue #4)
**Goals**: Lab environment, testing setup, API validation
- [ ] CHR (Cloud Hosted Router) setup guide
- [ ] Test log generator
- [ ] API connection validation
- [ ] Local testing setup

**AI Assistant Skills Needed**:
- Infrastructure setup
- Testing environment configuration
- Debugging & troubleshooting
- Documentation for reproducibility

**Prompt Examples**:
```
"Buatin script untuk generate mock SSH/FTP logs untuk testing. Format harus sesuai real MikroTik logs."

"Gimana cara test MikroTik API connection dari Python? Buatin simple connection test script."

"Setup CHR untuk lab environment. Apa steps yang diperlukan dan konfigurasi apa yang perlu?"
```

---

### Phase 4: IMPLEMENTATION (Future - Not started yet)
**Goals**: Write production code
- [ ] MikroTik API client module
- [ ] Log parser module
- [ ] Threat detection engine
- [ ] Firewall manager module
- [ ] Alert system module
- [ ] Main orchestration script
- [ ] Error handling & retries

**AI Assistant Skills Needed**:
- Python development
- API client implementation
- Data parsing & processing
- Error handling best practices
- Code review & optimization

**Prompt Examples**:
```
"Implement MikroTik API client. Support authenticate, get address-list, add/remove addresses."

"Buat log parser untuk extract SSH login attempts dari syslog. Output: {timestamp, username, ip, status}"

"Implement exponential backoff retry mechanism untuk API calls."
```

---

### Phase 5: MONITORING (Future - Not started yet)
**Goals**: Testing, validation, performance evaluation
- [ ] Unit tests untuk setiap modul
- [ ] Integration tests dengan router
- [ ] Performance benchmarks
- [ ] Penetration testing
- [ ] A/B testing untuk detection rules

**AI Assistant Skills Needed**:
- Test case design
- Performance benchmarking
- Security testing
- Data analysis

**Prompt Examples**:
```
"Design unit tests untuk threat detector. Test cases untuk: normal traffic, slow brute force, fast brute force, CPU anomaly"

"Buatin penetration test scenarios untuk validate system. Simulate: SSH brute force, FTP attack, malware behavior"

"Analyze performance metrics. MTTR target < 5 detik. Gimana cara measure dan optimize?"
```

---

### Phase 6: MANAGEMENT (Future - Not started yet)
**Goals**: Documentation, optimization, final report
- [ ] Complete technical documentation
- [ ] Optimization recommendations
- [ ] Deployment guide
- [ ] Final research report
- [ ] Lessons learned

**AI Assistant Skills Needed**:
- Technical writing
- Data analysis & interpretation
- Recommendations & best practices
- Report generation

**Prompt Examples**:
```
"Analyze hasil testing dan identify optimization opportunities untuk MTTR dan ADR."

"Buatin deployment guide untuk production. Include: prerequisites, setup, configuration, monitoring, troubleshooting"

"Generate technical report untuk Phase 1-6. Include: methodology, findings, results, recommendations"
```

---

## 🔧 DEVELOPMENT WORKFLOW

### For Vibes Coders: How to Maximize AI Assistance

#### 1. **Prompt Strategy**
```
❌ Jangan: "Bikin modul API"
✅ Sebaiknya: "Implement MikroTik API client module dengan methods: 
   - authenticate(host, user, pass)
   - get_address_list(name)
   - add_address(name, address, comment)
   - remove_address(name, address)
   Gunakan SSL, handle connection timeout, add retry logic"
```

#### 2. **Use Phase Context**
Selalu mention fase mana yang sedang dikerjakan:
```
"Phase 3: SIMULATION - Buatin CHR setup script untuk testing MikroTik API locally"
```

#### 3. **Provide Examples/Templates**
Berikan contoh format atau struktur yang diinginkan:
```
"Generate mock log sesuai format ini:
{timestamp} SSH failed-attempt [192.168.1.100] user: admin
```

#### 4. **Ask for Validation**
Minta AI untuk validasi implementasi:
```
"Validasi function ini. Ada edge cases yang terlewat? Bisa di-optimize?"
```

#### 5. **Documentation-First Approach**
Minta dokumentasi bersamaan dengan code:
```
"Implement function + dokumentasi lengkap (docstring, parameters, return, exceptions)"
```

---

## 📁 PROJECT STRUCTURE REFERENCE

```
TME-CORE/
├── .github/SKILL.md          ← You are here
├── BEGINNERS.md              ← Panduan untuk pemula
├── CONTRIBUTING.md           ← Contribution guidelines
├── README.md                 ← Main documentation
├── requirements.txt
├── .env.example
├── main.py
├── config.py
├── modules/
│   ├── mikrotik_api.py      ← Phase 4 (Implementation)
│   ├── log_parser.py        ← Phase 4 (Implementation)
│   ├── threat_detector.py   ← Phase 4 (Implementation)
│   ├── firewall_manager.py  ← Phase 4 (Implementation)
│   └── telegram_alert.py    ← Phase 4 (Implementation)
├── tests/
│   ├── test_api.py          ← Phase 5 (Monitoring)
│   ├── test_parser.py       ← Phase 5 (Monitoring)
│   └── test_detector.py     ← Phase 5 (Monitoring)
├── docs/
│   ├── ARCHITECTURE.md       ← Phase 2 (Design)
│   ├── API_REFERENCE.md      ← Phase 2 (Design)
│   ├── THREAT_MODEL.md       ← Phase 1 (Analysis)
│   └── TROUBLESHOOTING.md
└── logs/
    └── tme-core.log         ← Runtime logs
```

---

## 🎓 COMMUNICATION STYLE

### When Asking AI Assistant

**DO:**
- ✅ Be specific about what you want
- ✅ Provide context & requirements
- ✅ Ask for step-by-step explanations
- ✅ Request code with documentation
- ✅ Ask for validation & improvements
- ✅ Use Indonesian language
- ✅ Reference the current NDLC phase

**DON'T:**
- ❌ Generic/vague requests
- ❌ Assume AI knows your project details
- ❌ Ask for entire project at once
- ❌ Skip requirements/specifications
- ❌ Accept first solution without validation

### Expected Response Quality

**AI should provide:**
1. **Understanding** - Confirm understanding of requirements
2. **Solution** - Clear, working code/documentation
3. **Explanation** - Why this approach, alternatives considered
4. **Validation** - Edge cases, error handling
5. **Documentation** - Comments, docstrings, usage examples

**If not satisfied:**
- Ask for clarification
- Request different approach
- Ask for optimization
- Request more comprehensive solution

---

## 📊 REFERENCE: NDLC PHASES

```
PHASE 1: ANALYSIS (Current - Issue #2)
├─ Threat identification
├─ Requirement gathering
├─ Metrics definition
└─ Goal: Clear specification

PHASE 2: DESIGN (Issue #3)
├─ Architecture design
├─ API specification
├─ Database schema
└─ Goal: Technical blueprint

PHASE 3: SIMULATION (Issue #4)
├─ Lab environment setup
├─ Component testing
├─ Integration testing
└─ Goal: Validated environment

PHASE 4: IMPLEMENTATION (Future)
├─ Code development
├─ Integration
├─ Bug fixing
└─ Goal: Working system

PHASE 5: MONITORING (Future)
├─ Performance testing
├─ Security testing
├─ Load testing
└─ Goal: Performance metrics

PHASE 6: MANAGEMENT (Future)
├─ Documentation
├─ Optimization
├─ Final reporting
└─ Goal: Production ready
```

---

## 🔗 USEFUL RESOURCES FOR AI ASSISTANT

**Documentation to Reference:**
- [MikroTik API Manual](https://wiki.mikrotik.com/wiki/Manual:API)
- [RouterOS-api Python Library](https://github.com/socialengineer/python-routeros)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Best Practices](https://www.python.org/dev/peps/pep-0008/)

**Common Commands:**
```bash
# Testing MikroTik connection
python -c "from routeros_api import Api; print('✅ RouterOS-api works')"

# Generate mock data
python tests/generate_mock_logs.py

# Run tests
python -m pytest tests/ -v

# Check code quality
pylint modules/*.py
```

---

## 🚀 QUICK REFERENCE: WHAT TO ASK

### Phase 1: Analysis
```
"Analisa requirement untuk [specific threat/feature]. Output: detailed specification document"
"Design threat model untuk attack scenarios pada SSH/FTP"
"Define metrics dan KPI untuk sistem mitigasi"
```

### Phase 2: Design
```
"Design architecture untuk [component]. Output: diagram + detailed specification"
"Create API specification untuk [function/module]"
"Design database schema (jika diperlukan) untuk [use case]"
```

### Phase 3: Simulation
```
"Buatin setup guide untuk CHR di Proxmox/VirtualBox"
"Generate mock logs untuk testing [detection type]"
"Validate API connection procedure"
```

### Phase 4: Implementation
```
"Implement [module name] dengan specifications [detailed specs]. Include: error handling, logging, docstrings"
"Code review: Ada issues/improvements untuk code ini?"
"Optimize function untuk performance: [specific requirement]"
```

### Phase 5: Monitoring
```
"Design test cases untuk [module]. Cover: normal, edge cases, error scenarios"
"Analyze performance: MTTR adalah [current], target [target]. Recommendations?"
"Penetration test scenarios untuk validate detection accuracy"
```

### Phase 6: Management
```
"Generate technical report untuk [phase/component]"
"Analyze results dan provide optimization recommendations"
"Create deployment guide untuk production"
```

---

**Last Updated:** April 2026 | **Version:** 1.0 | **For:** Vibes Coders & AI Assistants
