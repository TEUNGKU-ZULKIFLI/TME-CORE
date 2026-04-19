# 📋 PROJECT PLANNING & ROADMAP

**TME-CORE Development Roadmap**

Dokumen ini memetakan langkah-langkah pengembangan berdasarkan NDLC Framework.

---

## 📊 CURRENT STATUS

| Phase | Status | Issues | Target Completion |
|-------|--------|--------|-------------------|
| **Phase 1: Analysis** | 🔴 In Progress | #1, #2 | Week 1 (Apr 19-25) |
| **Phase 2: Design** | ⚪ Queued | #1, #3 | Week 2-3 (Apr 26-May 3) |
| **Phase 3: Simulation** | ⚪ Queued | #1, #4 | Week 4-5 (May 4-11) |
| **Phase 4: Implementation** | ⚪ Not Started | To Create | Week 6-12 |
| **Phase 5: Monitoring** | ⚪ Not Started | To Create | Week 13-16 |
| **Phase 6: Management** | ⚪ Not Started | To Create | Week 17-20 |

---

## 🎯 PHASE 1: ANALYSIS (Issue #2)

### Goals
- [x] Define project scope & objectives
- [ ] Identify threats & attack patterns
- [ ] Define detection requirements
- [ ] Establish metrics & baselines
- [ ] Document assumptions & constraints

### Deliverables
- [ ] `docs/THREAT_MODEL.md` - Threat scenarios & attack patterns
- [ ] `docs/REQUIREMENTS.md` - Functional & non-functional requirements
- [ ] `docs/METRICS.md` - Performance metrics & KPIs
- [ ] `docs/ASSUMPTIONS.md` - Constraints & assumptions

### Tasks (Subtasks untuk #2)

#### Task 1: Threat Modeling
**AI Prompt:** "Analyze threat scenarios for TME-CORE. What are the main attack patterns on SSH (port 22) and FTP (port 21)? Create a threat matrix with: Attack Type | Severity | Frequency | Impact"

**Deliverable:** `docs/THREAT_MODEL.md`

**Acceptance Criteria:**
- Minimum 5 threat scenarios documented
- Each with: description, attack flow, indicators
- Clear severity levels (Critical/High/Medium/Low)

#### Task 2: Requirements Definition
**AI Prompt:** "Define functional and non-functional requirements for brute force detection system. Include: Detection requirements, Performance SLAs (MTTR < 5s), Scalability, Reliability, Security requirements"

**Deliverable:** `docs/REQUIREMENTS.md`

**Acceptance Criteria:**
- Functional requirements (what system must do)
- Non-functional requirements (performance, security, etc.)
- Prioritized by importance (Must Have / Should Have / Nice to Have)

#### Task 3: Metrics Definition
**AI Prompt:** "Define NDLC metrics for this project: MTTR (target < 5 sec), ADR (target 100%), CPU Offload (target > 60%), Network Stability. For each metric: definition, measurement method, baseline, target"

**Deliverable:** `docs/METRICS.md`

**Acceptance Criteria:**
- Clear metric definitions
- Measurement/collection method
- Current baseline (if available)
- Target values

### Success Criteria for Phase 1
- [ ] All threat scenarios documented
- [ ] Requirements approved
- [ ] Metrics defined & measurable
- [ ] Assumptions documented
- [ ] Stakeholder approval

### Estimated Duration
**2-3 weeks** (current progress: Week 1)

---

## 🛠️ PHASE 2: DESIGN (Issue #3)

### Goals
- [ ] Create system architecture
- [ ] Design API specifications
- [ ] Define module interfaces
- [ ] Create flow diagrams
- [ ] Design test strategy

### Deliverables
- [ ] `docs/ARCHITECTURE.md` - System architecture & components
- [ ] `docs/API_REFERENCE.md` - API specifications
- [ ] `docs/MODULE_DESIGN.md` - Module interfaces & design
- [ ] `docs/FLOW_DIAGRAMS.md` - Process flows (ASCII/Mermaid)
- [ ] `docs/DATABASE_SCHEMA.md` - If needed

### Tasks (Subtasks untuk #3)

#### Task 1: Architecture Design
**AI Prompt:** "Design the system architecture for TME-CORE. Include: Components (API Client, Parser, Detector, Firewall Manager, Alert), Data flow, Communication protocols, Error handling strategy. Output: Detailed architecture diagram + description"

**Deliverable:** `docs/ARCHITECTURE.md` dengan diagram

**Acceptance Criteria:**
- Clear component responsibilities
- Data flow documented
- Error handling strategy
- Scalability considerations

#### Task 2: API Specification
**AI Prompt:** "Spec-kan MikroTik API client requirements: Methods needed (authenticate, get_address_list, add_address, remove_address, etc.). For each method: parameters, return values, error cases, timeout handling, retry strategy"

**Deliverable:** `docs/API_REFERENCE.md`

**Acceptance Criteria:**
- All required API methods specified
- Parameter validation rules
- Error handling documented
- Examples provided

#### Task 3: Module Design
**AI Prompt:** "Design module structure for: 1) Log Parser - extract SSH/FTP logs, 2) Threat Detector - analyze patterns, 3) Firewall Manager - manage rules, 4) Alert System - send notifications. For each: interfaces, dependencies, error handling"

**Deliverable:** `docs/MODULE_DESIGN.md`

**Acceptance Criteria:**
- Module responsibilities clear
- Public interfaces defined
- Dependencies mapped
- Error handling documented

#### Task 4: Flow Diagrams
**AI Prompt:** "Create sequence diagrams for: 1) Brute force detection flow, 2) Anomaly detection flow, 3) Alert notification flow. Use Mermaid syntax for easy integration"

**Deliverable:** `docs/FLOW_DIAGRAMS.md`

**Acceptance Criteria:**
- All major flows documented
- Clear decision points
- Error paths shown
- Performance considerations noted

### Success Criteria for Phase 2
- [ ] Architecture reviewed & approved
- [ ] API specs complete & validated
- [ ] Module design finalized
- [ ] Design docs peer-reviewed
- [ ] Baseline for Phase 3 ready

### Estimated Duration
**2-3 weeks**

### Dependencies
- Completion of Phase 1 (Analysis)

---

## 🧪 PHASE 3: SIMULATION (Issue #4)

### Goals
- [ ] Setup lab environment
- [ ] Validate API connectivity
- [ ] Create test data generators
- [ ] Perform integration testing
- [ ] Establish baseline metrics

### Deliverables
- [ ] Lab environment setup (CHR instance)
- [ ] `tests/generate_mock_logs.py` - Mock log generator
- [ ] `tests/test_api_connection.py` - API connectivity tests
- [ ] `docs/LAB_SETUP.md` - Lab setup guide
- [ ] Performance baseline data

### Tasks (Subtasks untuk #4)

#### Task 1: Lab Environment Setup
**AI Prompt:** "Create step-by-step guide for setting up MikroTik CHR (Cloud Hosted Router) on VirtualBox/Proxmox for testing TME-CORE. Include: download, installation, basic config, API enablement"

**Deliverable:** `docs/LAB_SETUP.md`

**Acceptance Criteria:**
- Clear, reproducible steps
- Screenshots/diagrams where helpful
- Troubleshooting section
- Configuration checklists

#### Task 2: Mock Log Generator
**AI Prompt:** "Implement log generator for testing. Generate mock SSH/FTP logs in MikroTik syslog format. Scenarios: normal traffic, slow brute force (5/min), fast brute force (20/min), anomalous CPU usage. Output to file that can be imported"

**Deliverable:** `tests/generate_mock_logs.py`

**Acceptance Criteria:**
- Generates realistic logs
- Multiple scenarios supported
- Configurable parameters
- Output in correct format

#### Task 3: API Connectivity Tests
**AI Prompt:** "Write Python test script to validate MikroTik API connectivity: 1) Connect with credentials, 2) Get address-list, 3) Add/remove test address, 4) Test firewall rules, 5) Cleanup. Include error handling & timeout"

**Deliverable:** `tests/test_api_connection.py`

**Acceptance Criteria:**
- All API operations tested
- Error scenarios handled
- Cleanup performed
- Results logged

#### Task 4: Integration Testing
**AI Prompt:** "Design integration tests for: 1) Log parsing with mock data, 2) Threat detection with various log patterns, 3) Firewall rule creation, 4) Alert triggering. Include test data fixtures"

**Deliverable:** `tests/integration/` directory with test suite

**Acceptance Criteria:**
- Tests executable & passing
- Good coverage (>80%)
- Edge cases included
- Performance validated

### Success Criteria for Phase 3
- [ ] Lab environment operational
- [ ] All test scripts passing
- [ ] API connectivity validated
- [ ] Performance baseline established
- [ ] Ready for Phase 4 (Implementation)

### Estimated Duration
**2-3 weeks**

### Dependencies
- Completion of Phase 2 (Design)

---

## 💻 PHASE 4: IMPLEMENTATION (Future)

### Goals
- [ ] Implement all modules
- [ ] Integrate components
- [ ] Implement error handling
- [ ] Add logging & monitoring
- [ ] Performance optimization

### Planned Modules
1. **mikrotik_api.py** - MikroTik API client
2. **log_parser.py** - SSH/FTP log parser
3. **threat_detector.py** - Detection engine
4. **firewall_manager.py** - Firewall rule manager
5. **telegram_alert.py** - Alert system
6. **main.py** - Orchestration & main loop

### Estimated Duration
**6-8 weeks**

### Dependencies
- Completion of Phase 3 (Simulation)

---

## 🧪 PHASE 5: MONITORING (Future)

### Goals
- [ ] Comprehensive unit testing
- [ ] Performance testing & optimization
- [ ] Security testing
- [ ] Load testing
- [ ] Real-world validation

### Deliverables
- [ ] Unit test suite (>90% coverage)
- [ ] Performance test results
- [ ] Security audit report
- [ ] Optimization recommendations

### Estimated Duration
**4-6 weeks**

### Dependencies
- Completion of Phase 4 (Implementation)

---

## 📚 PHASE 6: MANAGEMENT (Future)

### Goals
- [ ] Complete documentation
- [ ] Optimization & tuning
- [ ] Deployment preparation
- [ ] Final reporting
- [ ] Knowledge transfer

### Deliverables
- [ ] Deployment guide
- [ ] Operations manual
- [ ] Final research report
- [ ] Lessons learned document

### Estimated Duration
**3-4 weeks**

### Dependencies
- Completion of Phase 5 (Monitoring)

---

## 🚀 QUICK ACTIONS FOR NEXT 7 DAYS

### Priority 1: Complete Phase 1 Tasks
- [ ] **Threat Modeling** - Document all attack scenarios
- [ ] **Requirements Definition** - Define what system must do
- [ ] **Metrics Definition** - Clear measurement criteria

### Priority 2: Prepare Phase 2
- [ ] Review threat model with stakeholders
- [ ] Start architecture design thinking
- [ ] Research MikroTik API capabilities

### Priority 3: Project Documentation
- [ ] ✅ README.md updated ✓
- [ ] ✅ .github/SKILL.md created ✓
- [ ] ✅ BEGINNERS.md created ✓
- [ ] ⚠️ Setup local environment testing
- [ ] ⚠️ Validate all configurations work

---

## 📊 SUCCESS METRICS

### Overall Project Success Criteria

| Metric | Target | Measurement |
|--------|--------|------------|
| Phase Completion Rate | 100% | On-time delivery of phases |
| Code Quality | >90% | Code review & linting |
| Test Coverage | >85% | Automated test suite |
| Documentation | Complete | All docs peer-reviewed |
| MTTR Achievement | < 5 sec | Measured in Phase 5 |
| ADR Achievement | 100% | Measured in Phase 5 |

---

## 🔄 WEEKLY STANDUP TEMPLATE

```markdown
## Week X Standup (YYYY-MM-DD)

### Completed This Week
- [ ] Task 1
- [ ] Task 2

### In Progress
- [ ] Task 3
- [ ] Task 4

### Blockers
- [ ] Issue/blocker description

### Plan for Next Week
- [ ] Task 5
- [ ] Task 6

### Notes
- Additional context
```

---

## 👥 ROLES & RESPONSIBILITIES

| Role | Responsibility | Current |
|------|-----------------|---------|
| **Project Lead** | Roadmap, milestone tracking, decisions | Teungku Zulkifli |
| **Vibes Coder** | Implementation, AI-assisted development | You |
| **AI Assistant** | Analysis, code generation, documentation | GitHub Copilot (This) |
| **Reviewer** | Code review, quality assurance | TBD |

---

**Last Updated:** April 2026 | **Next Review:** April 25, 2026
