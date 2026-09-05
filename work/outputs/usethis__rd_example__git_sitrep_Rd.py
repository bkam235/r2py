# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import subprocess

# r2py:entity:git_sitrep
def git_sitrep():
    try:
        # Equivalent to checking git status and config
        print("--- Git Status ---")
        subprocess.run(["git", "status"], check=True)
        
        print("\n--- Git User Config ---")
        subprocess.run(["git", "config", "user.name"], check=True)
        subprocess.run(["git", "config", "user.email"], check=True)
    except subprocess.CalledProcessError:
        print("Git is not installed or not configured in this directory.")

git_sitrep()