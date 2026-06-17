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
    elif event.kind == "iteration_start" and VERBOSE:
        print(f"[Iter {event.iteration + 1}] Best score so far: {event.score:.3f}")
    elif event.kind == "proposal" and VERBOSE and event.edit_kind != "RetranslateEntity":
        print(f"          {event.edit_kind} on {event.entity_id!r} -> {event.outcome} ({event.score:.3f})")
    elif event.kind == "retranslation_start" and VERBOSE:
        print(f"[Retry]   Plateau detected — retranslating from scratch (score: {event.score:.3f})")
    elif event.kind == "retranslation_done" and VERBOSE:
        print(f"[Retry]   Retranslation scored: {event.score:.3f}")
    elif event.kind == "done":
        print(f"[Done]    Final score: {event.score:.3f} in {event.iteration} iteration(s)")


# Iterate through input files for translation
input_filenames = next(walk(input_dir), (None, None, []))[2]
# input_filenames = random.sample(input_filenames, 1) #don't use random script

input_filenames = ["bit__rd_example__chunk_Rd.R"] #translate this specific script
# input_filenames = ["shape__rd_example__greycol_Rd.R", "withr__rd_example__with_locale_Rd.R, xfun__rd_example__cache_rds_Rd.py"]

# shape__rd_example__greycol_Rd.R 0.930
# withr__rd_example__with_locale_Rd.R 0.987
# xfun__rd_example__cache_rds_Rd.py 0.927
# googlesheets4__rd_example__sheet_append_Rd.R 0.992
# progressr__rd_example__handler_rpushbullet_Rd.R 0.990

# from r2py import seed_from_translation
# seed_from_translation(
#     "work/inputs/harvested/withr__rd_example__with_locale_Rd.R",
#     "work/outputs/withr__rd_example__with_locale_Rd.py",
# )

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
                       model="claude-haiku-4-5",
                    #    model="ollama:gemma4:31b-cloud",
                       progress=_on_progress,
                       score_threshold=0.9,
                       max_iters=5,
                       retranslation_patience=3,
                       n_seeds=3)

