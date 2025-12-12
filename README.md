# z3-verify-directory
Z3 filesystem integrity verifier ensures no directory files modified after cutoff timestamp like "2025-12-05 14:30:00". Recursively walks tree with os.walk, binds each getmtime to Real vars, constrains ≤ cutoff. unsat proves compliance; sat shows tampering model. For secure baseline auditing.
This Python script implements a Z3 SMT-based formal verifier for filesystem integrity, recursively auditing all files in a directory tree to prove none were modified after a user-specified cutoff timestamp (e.g., "2025-12-05 14:30:00").

Detailed Verification Process
The function parses the cutoff into an epoch timestamp as a Z3 RealVal. It uses os.walk to traverse the directory, fetching each file's actual modification time via os.path.getmtime. For every file, it creates a unique Real variable (e.g., mtime_filename_0), binds it exactly to the real mtime with ==, and constrains it to ≤ cutoff. This encodes the universal policy ∀ files: mtime ≤ cutoff.

SMT Semantics and Output
s.check() tests satisfiability under these constraints. unsat mathematically proves compliance (no model exists violating the policy), printing the file count and timestamp. sat detects tampering, outputting the concrete counterexample model (specific file variables exceeding cutoff). Returns boolean result for automation.

Cybersecurity Applications
Perfect for baseline integrity checks in secure environments—like verifying production deployments, compliance audits, or tamper detection against known-good states. The arbitrary cutoff enables reproducible audits independent of runtime, leveraging Z3's provable guarantees over heuristic checks. Handles full directory trees efficiently.
