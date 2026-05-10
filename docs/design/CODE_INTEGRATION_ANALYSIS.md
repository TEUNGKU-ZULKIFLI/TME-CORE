# Code Integration Analysis - Module Dependencies

## Module Dependency Graph

```
config.py
  ├─ Load app_config.yaml
  └─ Return config dict
     │
     ├── engine.py
     │   ├─ Load config
     │   ├─ Init API client
     │   ├─ Init log parser
     │   ├─ Init detectors (Jalur A + B)
     │   └─ Main loop
     │
     ├── api/mikrotik_client.py
     │   ├─ Connect to API
     │   ├─ block_ip()
     │   ├─ get_router_cpu()
     │   └─ Return response times
     │
     ├── parser/log_parser.py
     │   ├─ Read log file from config
     │   ├─ Stream events
     │   └─ Yield LoginEvent objects
     │
     ├── detection/brute_force_detector.py
     │   ├─ Input: LoginEvent stream
     │   ├─ Check threshold from config
     │   └─ Output: is_threat boolean
     │
     └── detection/anomaly_detector.py
         ├─ Input: LoginEvent + CPU data
         ├─ Check thresholds from config
         └─ Output: is_anomaly boolean
```

## Data Flow Integration

1. **Initialization Phase**
   ```
   config.py ──→ engine.py
   engine.py ──→ api/mikrotik_client.py (connect)
   engine.py ──→ parser/log_parser.py (open file)
   engine.py ──→ detection/brute_force_detector.py (init)
   engine.py ──→ detection/anomaly_detector.py (init)
   ```

2. **Main Loop**
   ```
   parser.stream_events() ────┐
                               ├─ engine.start()
   api.get_router_cpu() ──────┤
                               ├─ detection/brute_force_detector.process_event()
                               ├─ detection/anomaly_detector.process_event()
                               ├─ If threat: api.block_ip()
                               └─ Save metrics
   ```

## Current Integration Status

| Module | Status | Integration | Notes |
|--------|--------|-------------|-------|
| config.py | ✅ | engine.py | YAML loader working |
| logger.py | ✅ | All modules | Logging configured |
| exceptions.py | ✅ | api/parser/detectors | Custom exceptions used |
| api/mikrotik_client.py | ✅ | engine.py | API connect & block working |
| parser/log_parser.py | ✅ | engine.py | Real-time streaming verified |
| detection/brute_force_detector.py | ✅ | engine.py | Tested with real attacks |
| detection/anomaly_detector.py | ⚠️ | engine.py (partial) | Template ready, full integration TBD |
| engine.py | ✅ | All | Main orchestrator, 9-min test passed |
| firewall/ (future) | ❌ | Planned | Will refactor blocking logic |
| alert/ (future) | ❌ | Planned | Will add Telegram alerts |

## Folder Usage Summary

```yaml
config/:
  - app_config.yaml: ✅ Active (log paths, thresholds)
  - .env.example: ✅ Active (template)
  - .env: ⏳ Local only (secrets)

src/:
  - ✅ All Python modules actively used
  - ✅ Modular structure allows future expansion
  - ⏳ firewall/ & alert/ reserved for Phase 4

scripts/:
  - test_api_connection.py: ✅ Phase 1 artifact (still useful for verification)

tests/:
  - ⏳ Empty (unit tests to be added Phase 4)

data/:
  - logs/: ✅ Runtime logs (ephemeral)
  - metrics/: ✅ Results tracking (archival)
  - samples/: ✅ Real attack logs (immutable samples)
  - db/: ⏳ Reserved for Phase 4 (SQLite)

docs/:
  - ✅ All markdown files (ARCHITECTURE, SETUP_LAB, THREAT_ANALYSIS)
  - ⏳ design/ subdirectory (Phase 3 - active now)
  - ⏳ diagrams/ (UML files)

thesis/:
  - ⏳ Empty (to be populated Phase 4 onward with skripsi chapters)
```

## Recommendation: Phase 4 Refactoring

Before extensive testing, recommend:
1. Extract blocking logic → `firewall/firewall_manager.py`
2. Extract alerting → `alert/telegram_bot.py`
3. Add unit tests → `tests/unit/`
4. Add integration tests → `tests/integration/`
5. Consider SQLite for persistent metrics → `data/db/`