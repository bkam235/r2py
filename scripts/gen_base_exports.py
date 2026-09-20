"""Regenerate r2py/stage1/base_exports.json: the functions exported by the packages R attaches
by default, keyed by package. Stage 1 uses it to recognise base-R calls inside entities.

    python scripts/gen_base_exports.py

Run it again when the bundled R runtime changes (the R version is recorded in the file).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from r2py.stage0.env.r_runtime import find_rscript

# Listed in priority order: a name exported by several packages is keyed to the first.
PACKAGES = ["base", "stats", "utils", "graphics", "grDevices", "methods"]

R_CODE = """
cat('R_VERSION', R.version.string, '\\n')
for (p in c(%s)) {
  env <- as.environment(paste0('package:', p))
  for (n in ls(env, all.names = FALSE)) if (is.function(get(n, envir = env))) cat(p, n, '\\n')
}
""" % ", ".join(f"'{p}'" for p in PACKAGES)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:  # a script file: multi-line -e crashes Rscript on Windows
        script = Path(tmp) / "exports.R"
        script.write_text(R_CODE, encoding="utf-8")
        out = subprocess.run([str(find_rscript()), "--vanilla", str(script)],
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
    packages: dict[str, list[str]] = {p: [] for p in PACKAGES}
    version = ""
    for line in out.splitlines():
        parts = line.split()
        if parts[:1] == ["R_VERSION"]:
            version = " ".join(parts[1:])
        elif len(parts) == 2 and parts[0] in packages:
            packages[parts[0]].append(parts[1])
    packages = {p: sorted(set(names)) for p, names in packages.items()}
    path = ROOT / "r2py" / "stage1" / "base_exports.json"
    path.write_text(json.dumps({"r_version": version, "packages": packages}, indent=0) + "\n",
                    encoding="utf-8")
    print(f"{version}: " + ", ".join(f"{p}={len(n)}" for p, n in packages.items()) + f" -> {path}")


if __name__ == "__main__":
    main()
