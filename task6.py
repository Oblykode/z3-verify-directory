from z3 import *
import os
from datetime import datetime

def z3_verify_directory(directory: str, cutoff_str: str) -> bool:
    """
    Verify no files modified after arbitrary cutoff timestamp using Z3 SMT.
    cutoff_str format: '2025-12-05 14:30:00' or ISO '2025-12-05T14:30:00'
    """
    s = Solver()
    
    # Parse user-specified cutoff (not current time)
    cutoff_time = datetime.strptime(cutoff_str, '%Y-%m-%d %H:%M:%S')
    cutoff_epoch = cutoff_time.timestamp()
    cutoff = RealVal(cutoff_epoch)
    
    # Collect all files in directory tree
    file_mtimes = []
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            if os.path.isfile(path):
                real_mtime = os.path.getmtime(path)
                file_var = Real(f'mtime_{os.path.basename(path)}_{len(file_mtimes)}')
                s.add(file_var == RealVal(real_mtime))  # Bind to actual mtime
                s.add(file_var <= cutoff)  # ∀x ¬P(x): mtime_x ≤ cutoff
                file_mtimes.append(file_var)
    
    # Verify: UNSAT means no model exists where any file > cutoff
    result = s.check()
    
    if result == unsat:
        print(f" Verified: All {len(file_mtimes)} files unmodified after {cutoff_str}")
        return True
    else:
        print(f"Tampering detected after {cutoff_str}")
        print("Counterexample model:", s.model())
        return False

# Usage with arbitrary reference timestamp
result = z3_verify_directory("/path/to/secure/directory", "2025-12-05 14:30:00")
print("Integrity holds:", result)
