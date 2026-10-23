# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 12

import ps
import subprocess
import time

# The R example uses processx::process$new("sleep", "100").
# In Python, we can use subprocess.Popen.
# ps.Process handles wrapping these existing PIDs.

# r2py:entity:ps_is_supported
try:
    # p1 <- processx::process$new("sleep", "100")
# r2py:entity:p1
    p1_proc = subprocess.Popen(["sleep", "100"])
    p1 = ps.Process(p1_proc.pid)

    # p2 <- processx::process$new("sleep", "100")
# r2py:entity:p2
    p2_proc = subprocess.Popen(["sleep", "100"])
    p2 = ps.Process(p2_proc.pid)

    # ps_wait(list(p1$as_ps_handle(), p2$as_ps_handle()), 0)
    # In R's ps package, ps_wait returns a logical vector indicating if processes terminated.
    # Python's psutil doesn't have a direct multi-process 'wait' with timeout that returns 
    # a boolean list like ps_wait. We implement the equivalent logic.
# r2py:entity:ps_wait
    def ps_wait(processes, timeout_ms):
        start_time = time.time()
        timeout_sec = timeout_ms / 1000.0
        
        # Convert timeout 0 to immediate check
        # Convert -1 to indefinite wait (though the example uses 0 and 1000)
        
        while True:
            results = [not p.is_running() for p in processes]
            if all(results):
                return results
            
            if timeout_ms == 0:
                return results
            
            if timeout_ms != -1 and (time.time() - start_time) >= timeout_sec:
                return results
            
            if timeout_ms == -1 and all(results):
                return results
                
            time.sleep(0.01) # Prevent busy loop

    # returns [False, False] immediately if p1 and p2 are running
    print(ps_wait([p1, p2], 0))

    # timeouts at one second
# r2py:entity:ps_wait_1
    print(ps_wait([p1, p2], 1000))

    # p1$kill()
# r2py:entity:p1$kill
    p1_proc.kill()
    # p2$kill()
# r2py:entity:p2$kill
    p2_proc.kill()

    # returns [True, True] immediately
# r2py:entity:ps_wait_2
    print(ps_wait([p1, p2], 1000))

except Exception as e:
    print(f"Error executing sleep example: {e}")
finally:
    # Ensure processes are cleaned up if they somehow survived
    for p in [p1_proc if 'p1_proc' in locals() else None, 
               p2_proc if 'p2_proc' in locals() else None]:
        if p:
            p.terminate()