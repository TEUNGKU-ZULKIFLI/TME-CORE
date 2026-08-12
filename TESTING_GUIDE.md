# TME-CORE: AKURASI THRESHOLD + PERSISTENCE TESTING GUIDE

## Pre-Test Setup

```bash
cd ~/TME-CORE

# 1. Reset state (clean slate)
rm -f data/db/tme_state.json
rm -f data/logs/tmecore_system.log
rm -f data/metrics/evaluasi_kinerja.csv

# 2. Ensure .env set dengan benar
cat .env | grep -E "MIKROTIK|WHITELIST|TELEGRAM"
```

## Test Case 1: BASIC THRESHOLD (9 attempts = NO BLOCK)

**Expected Behavior**:
- IP melakukan 9 gagal login
- Total: 9 < 10 threshold
- NO DETECTED warning
- State disimpan

**Execution**:
```bash
python3 -m src.main_engine &
ENGINE_PID=$!

# Simulate 9 failed attempts dari IP 192.168.20.50
for i in {1..9}; do
  ssh -o ConnectTimeout=1 admin@192.168.20.50 <<< "wrong_password" 2>/dev/null &
  sleep 0.5
done

sleep 3
kill $ENGINE_PID

# Verification
echo "=== Checking log ==="
tail -15 data/logs/tmecore_system.log
grep "192.168.20.50" data/logs/tmecore_system.log | tail -3
grep "DETECTED" data/logs/tmecore_system.log || echo "✅ NO DETECTED (Expected)"

echo "=== Checking state.json ==="
jq '.persistent_failed_counts."192.168.20.50"' data/db/tme_state.json
```

**Expected Log Output**:
```
Gagal login dari 192.168.20.50 (recent=0→1 | persist=0→1 | total=1)
Gagal login dari 192.168.20.50 (recent=1→2 | persist=1→2 | total=2)
...
Gagal login dari 192.168.20.50 (recent=8→9 | persist=8→9 | total=9)
[NO DETECTED]
```

**Expected state.json**:
```json
{
  "persistent_failed_counts": {
    "192.168.20.50": {"count": 9, "last": 1786561234.567}
  }
}
```

---

## Test Case 2: CUMULATIVE THRESHOLD (6 + 6 = 12 ≥ 10 BLOCK)

**Expected Behavior**:
- IP melakukan 6 gagal login
- Stop engine (Ctrl+C)
- Restart engine → Load: persist=6
- IP melakukan 6 gagal login lagi
- Total: 6 (recent) + 6 (persist) = 12 ≥ 10 threshold
- DETECTED on attempt 5-6
- IP diblokir

**Execution**:
```bash
# Round 1: Initial 6 attempts
python3 -m src.main_engine &
ENGINE_PID=$!

for i in {1..6}; do
  ssh -o ConnectTimeout=1 admin@192.168.20.51 <<< "wrong_password" 2>/dev/null &
  sleep 0.5
done

sleep 2
kill $ENGINE_PID

echo "✅ Round 1 complete. State saved."
tail -8 data/logs/tmecore_system.log

# Round 2: Restart dan 6 attempts lagi
sleep 2
python3 -m src.main_engine &
ENGINE_PID=$!

# Check load message
sleep 3
echo "=== Loading state ==="
head -20 data/logs/tmecore_system.log | tail -5

# Do 6 more attempts
for i in {1..6}; do
  ssh -o ConnectTimeout=1 admin@192.168.20.51 <<< "wrong_password" 2>/dev/null &
  sleep 0.5
done

sleep 3
kill $ENGINE_PID
```

**Expected Log Output**:
```
=== ROUND 1 ===
Gagal login dari 192.168.20.51 (recent=0→1 | persist=0→1 | total=1)
Gagal login dari 192.168.20.51 (recent=1→2 | persist=1→2 | total=2)
...
Gagal login dari 192.168.20.51 (recent=5→6 | persist=5→6 | total=6)

=== ROUND 2 (After Restart) ===
[✓] DATABASE RESTORED:
    ├─ Persistent Failure Counts (Threshold=10, Retention=3600s): 1
    │  └─ 192.168.20.51: 6/10 OK

Gagal login dari 192.168.20.51 (recent=0→1 | persist=6→7 | total=8)
Gagal login dari 192.168.20.51 (recent=1→2 | persist=7→8 | total=9)
Gagal login dari 192.168.20.51 (recent=2→3 | persist=8→9 | total=10 [Threshold: 10])
[⚠️] DETECTED: BRUTE_FORCE from 192.168.20.51 [Attempts: 10/10]
MITIGATED: IP 192.168.20.51 blocked in firewall
```

**Expected state.json after block**:
```json
{
  "persistent_failed_counts": {
    "192.168.20.51": {"count": 0, "last": 0}  ← RESET after block
  }
}
```

---

## Test Case 3: UNAUTHORIZED_SUCCESS (History + Login Sukses)

**Expected Behavior**:
- IP melakukan 5 gagal login
- IP melakukan 1 login SUKSES
- Total: 5 > 0 (ada history)
- DETECTED: UNAUTHORIZED_SUCCESS
- IP diblokir

**Execution**:
```bash
python3 -m src.main_engine &
ENGINE_PID=$!

# 5 failed attempts
for i in {1..5}; do
  ssh -o ConnectTimeout=1 admin@192.168.20.52 <<< "wrong_password" 2>/dev/null &
  sleep 0.5
done

sleep 2

# 1 successful login (if applicable in your test environment)
# Note: In real scenario, this would be detected via log

sleep 3
kill $ENGINE_PID
```

**Expected Log Output**:
```
Gagal login dari 192.168.20.52 (recent=0→1 | persist=0→1 | total=1)
...
Gagal login dari 192.168.20.52 (recent=4→5 | persist=4→5 | total=5)
[⚠️] DETECTED: UNAUTHORIZED_SUCCESS from 192.168.20.52 [Attempts: 5/10]
MITIGATED: IP 192.168.20.52 blocked + session kicked
```

---

## Verification Checklist

- [ ] **Compile**: All files compile without syntax errors
- [ ] **Test 1**: 9 attempts shows `total=9` without DETECTED
- [ ] **Test 2**: 6+6 cumulative triggers DETECTED at attempt 3-4 with `total≥10`
- [ ] **Test 2**: After block, persistent_failed_counts reset to `{"count": 0}`
- [ ] **Test 3**: SUCCESS after 5 failures triggers UNAUTHORIZED_SUCCESS
- [ ] **Restore**: Engine restart shows correct persistent count in "DATABASE RESTORED" log
- [ ] **Threshold Info**: "NEAR THRESHOLD" marker appears when count ≥ 8
- [ ] **Metrics CSV**: evaluasi_kinerja.csv records mitigation events

---

## Debug Commands

```bash
# Check latest log entries
tail -20 data/logs/tmecore_system.log

# Check state.json format
jq . data/db/tme_state.json

# Check IP-specific persistent count
jq '.persistent_failed_counts."192.168.20.50"' data/db/tme_state.json

# Check metrics CSV
tail -10 data/metrics/evaluasi_kinerja.csv

# Grep for specific keywords
grep "DETECTED\|Gagal login\|DATABASE RESTORED" data/logs/tmecore_system.log
```

---

## Expected Behavior Summary

| Scenario | Behavior | Threshold | Action |
|----------|----------|-----------|--------|
| 9 attempts | total=9 | < 10 | No block |
| 6 + 6 attempts (restart) | total=12 | ≥ 10 | BLOCK at attempt 3-4 |
| 5 failures + 1 success | total=5 | > 0 | BLOCK (UNAUTHORIZED_SUCCESS) |
| After block | reset | - | persistent_count = 0 |
| Whitelist IP | - | - | Always allow |

