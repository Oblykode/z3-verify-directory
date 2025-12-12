# z3-verify-directory
Z3 filesystem integrity verifier ensures no directory files modified after cutoff timestamp like "2025-12-05 14:30:00". Recursively walks tree with os.walk, binds each getmtime to Real vars, constrains ≤ cutoff. unsat proves compliance; sat shows tampering model. For secure baseline auditing. (312 chars)
