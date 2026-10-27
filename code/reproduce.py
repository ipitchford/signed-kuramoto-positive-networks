"""Rerun every Kuramoto check into a fresh output directory.

Usage (from the bundle root, Python 3.12 pinned in .python-version):
  uv run --no-project --python 3.12 --with-requirements requirements.txt \
      python -I code/reproduce.py --out OUTPUT_DIRECTORY [--pdf]

Nothing in checks/ or figures/ is overwritten.  The exact certificate and the
edge list are compared byte for byte with the shipped copies in checks/;
floating-point diagnostics are reported, not compared, because their last
digits depend on the platform's linear-algebra library.
"""
from pathlib import Path
import argparse
import filecmp
import json
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(args, out_file=None):
    res = subprocess.run([sys.executable, "-I", *args], cwd=ROOT, capture_output=True, text=True)
    if res.returncode:
        sys.stderr.write(res.stdout[-4000:] + res.stderr[-4000:])
        raise SystemExit(res.returncode)
    if out_file:
        out_file.write_text(res.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--pdf", action="store_true", help="also compile the manuscript inside OUT")
    a = ap.parse_args()
    out = a.out.resolve()
    if out == ROOT or ROOT / "checks" in [out, *out.parents] or ROOT / "figures" in [out, *out.parents]:
        raise SystemExit("Refusing to write into the shipped checks/ or figures/ directories.")
    out.mkdir(parents=True, exist_ok=True)
    import numpy, scipy, matplotlib
    (out / "runtime_versions.json").write_text(json.dumps(
        {"python": platform.python_version(), "numpy": numpy.__version__,
         "scipy": scipy.__version__, "matplotlib": matplotlib.__version__}, indent=2) + "\n")
    run(["code/verify_attractive_embedding.py"], out / "exact_kuramoto_certificate.txt")
    print("PASS exact certificate")
    run(["code/kuramoto_checks.py", "--out", str(out)])
    print("PASS floating and random-graph checks")
    run(["code/make_figures.py", "--out", str(out)])
    print("PASS figure")
    for name in ("exact_kuramoto_certificate.txt", "kuramoto_edges.csv"):
        same = filecmp.cmp(out / name, ROOT / "checks" / name, shallow=False)
        print(("IDENTICAL " if same else "DIFFERS ") + name)
        if not same:
            raise SystemExit(1)
    if a.pdf:
        build = out / "build"
        build.mkdir(exist_ok=True)
        shutil.copy(ROOT / "signed_kuramoto_networks_inside_positive_ones.tex", build)
        shutil.copytree(ROOT / "figures", build / "figures", dirs_exist_ok=True)
        for _ in range(2):
            res = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                  "signed_kuramoto_networks_inside_positive_ones.tex"], cwd=build,
                                 capture_output=True, text=True)
            if res.returncode:
                sys.stderr.write(res.stdout[-4000:])
                raise SystemExit(res.returncode)
        print("PASS pdf in", build)
    print("Complete. These checks support, and do not replace, the analytic proofs.")


if __name__ == "__main__":
    main()
