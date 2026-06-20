import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from r2py import translate, reset_library
from r2py.library import get_library
from dotenv import load_dotenv
from os import walk, path, listdir, remove, environ
import random

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

lib = get_library()  # one shared library
# reset_library(library=lib) # keep seeds, wipe learned patterns
# reset_library(library=lib, keep_seeds=False) #wipe everything

input_dir = r".\work\inputs\harvested"
output_dir = r".\work\outputs"

VERBOSE = True

def _on_progress(event) -> None:
    if event.kind == "analysis_done":
        print(f"[Stage 1] Analysis complete — {event.entity_count} entities")
    elif event.kind == "seed_done":
        print(f"[Seed]    Initial score: {event.score:.3f}")
    elif event.kind == "agent_start" and VERBOSE:
        print(f"[Agent]   Escalating to reasoning agent (seed score: {event.score:.3f})")
    elif event.kind == "seeded":
        print(f"[Seed]    Seeded {event.count} patterns from translation")
    elif event.kind == "done":
        print(f"[Done]    Final score: {event.score:.3f}")


# Iterate through input files for translation
input_filenames = next(walk(input_dir), (None, None, []))[2]
input_filenames = random.sample(input_filenames, 3) #don't use random script

# input_filenames = ["purrr__rd_example__lift_Rd.R"] #translate this specific script
# HARD CASES #
# purrr__rd_example__lift_Rd.R

scripts = []
for r_filename in input_filenames:
    file_prefix = r_filename.split(".")[0]
    py_filename = file_prefix + ".py"
    py_file_path = path.join(output_dir, py_filename)
    r_file_path = path.join(input_dir, r_filename)
    scripts.append((r_file_path, py_file_path))

for r_script, py_script in scripts:
    print("############################")
    print(f"{r_script}")
    print("############################")
    
    result = translate(r_script,
                       py_script,
                       library=lib,
                       resume=True,
                    #    model="claude-haiku-4-5",
                       model="ollama:gemma4:31b-cloud",
                    #    escalation_model="claude-haiku-4-5",
                       escalation_model="ollama:gemma4:31b-cloud",
                       progress=_on_progress,
                       score_threshold=0.95,
                       max_iters=15)

# from r2py import seed_from_translation
# seed_from_translation(
#     "work/inputs/harvested/purrr__rd_example__lift_Rd.R",
#     "work/outputs/purrr__rd_example__lift_Rd.py",
# )

# Hypothesis: I need repeated runs on the same script to make scores higher and reproducible
# First with stronger models, then after 3-5 re-runs Gemma does it right on seed