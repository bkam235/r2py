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
# input_filenames = random.sample(input_filenames, 20) #don't use random script

input_filenames = ["broom__rd_example__durbinWatsonTest_tidiers_Rd.R"] #translate this specific script

# all_translated_scripts = [
#     "S7__vignette__generics-methods_s13",
#     "bit__rd_example__chunk_Rd",
#     "bit__vignette__bit-usage_s15",
#     "broom__rd_example__durbinWatsonTest_tidiers_Rd",
#     "bslib__rd_example__popover_Rd",
#     "cli__rd_example__cat_line_Rd",
#     "clock__rd_example__duration_spanning_seq_Rd",
#     "clock__vignette__clock_s4",
#     "dplyr__rd_example__all_equal_Rd",
#     "dplyr__rd_example__storms_Rd",
#     "dplyr__vignette__in-packages_s3",
#     "dplyr__vignette__two-table_s13",
#     "dplyr__vignette__window-functions_s11",
#     "forcats__rd_example__lvls_Rd",
#     "ggplot2__rd_example__facet_wrap_Rd",
#     "glue__vignette__wrappers_s1",
#     "googlesheets4__rd_example__range_flood_Rd",
#     "googlesheets4__rd_example__sheet_append_Rd",
#     "haven__rd_example__print_labels_Rd",
#     "modelr__rd_example__typical_Rd",
#     "plyr__rd_example__splitter_a_Rd",
#     "prodlim__rd_example__row_match_Rd",
#     "progressr__rd_example__handler_rpushbullet_Rd",
#     "purrr__rd_example__keep_at_Rd",
#     "purrr__rd_example__lift_Rd",
#     "recipes__rd_example__step_profile_Rd",
#     "recipes__vignette__Roles_s1",
#     "rlang__rd_example__catch_cnd_Rd",
#     "rlang__rd_example__missing_Rd",
#     "shape__rd_example__greycol_Rd",
#     "shiny__rd_example__withOtelCollect_Rd",
#     "timeDate__rd_example__holiday_Rd",
#     "timeDate__rd_example__stats-na-fail_Rd",
#     "vctrs__rd_example__vec_fill_missing_Rd",
#     "vctrs__vignette__type-size_s21",
#     "withr__rd_example__with_locale_Rd",
#     "xfun__rd_example__cache_rds_Rd",
#     "xfun__rd_example__protect_math_Rd",
#     "xtable__rd_example__sanitize_Rd",
#     "xtable__rd_example__xtableFtable_Rd",
#     "xtable__vignette__listOfTablesGallery_s2",
# ]

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
    
    # trans_model = "ollama:gemma4:31b-cloud"
    trans_model = "claude-haiku-4-5"
    # trans_model = "claude-sonnet-4-6"


    result = translate(r_script,
                       py_script,
                       library=lib,
                       resume=True,
                       model=trans_model,
                       escalation_model=trans_model,
                       progress=_on_progress,
                       score_threshold=0.9,
                       max_iters=20,
                       max_stalls=5)

# from r2py import seed_from_translation
# seed_from_translation(
#     "work/inputs/harvested/purrr__rd_example__lift_Rd.R",
#     "work/outputs/purrr__rd_example__lift_Rd.py",
# )

# Hypothesis: I need repeated runs on the same script to make scores higher and reproducible
# First with stronger models, then after 3-5 re-runs Gemma does it right on seed