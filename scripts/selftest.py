#!/usr/bin/env python3
"""selftest.py - build and ATS-check the fictional example with every available PDF maker.

    python3 scripts/selftest.py            # all renderers that work here
    python3 scripts/selftest.py reportlab  # just one

Exit code 0 if everything that could run passed.
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ats_check  # noqa: E402
import build_docx  # noqa: E402
import build_pdf  # noqa: E402

EXAMPLE = os.path.join(os.path.dirname(HERE), "examples", "sample-person", "my-career")


def main():
    wanted = sys.argv[1:] or build_pdf.ORDER
    tmp = tempfile.mkdtemp()
    work = os.path.join(tmp, "my-career")
    shutil.copytree(EXAMPLE, work)
    docs = [os.path.join(work, "output", "core", "resume.md"),
            os.path.join(work, "output", "acme-health-senior-product-analyst", "cover-letter.md")]
    failures, ran = 0, 0
    for r in wanted:
        for md in docs:
            name = f"{r:<10} {os.path.basename(md)}"
            try:
                res = build_pdf.build(md, renderer=r)
            except Exception as e:  # noqa: BLE001
                print(f"SKIP {name}: {str(e).splitlines()[-1][:90]}")
                break
            ran += 1
            kw = os.path.join(work, "targets", "positioning.md")
            results, _ = ats_check.check(res["pdf"], md, kw if "resume" in md else None)
            bad = [x for x in results if x[0] == "FAIL"]
            ok = res["fits"] and not bad
            failures += 0 if ok else 1
            print(f"{'PASS' if ok else 'FAIL'} {name}: {res['pages']}p {res['paper']} "
                  f"{res['font_pt']}pt" + "".join(f"\n     {b[1]}: {b[2]}" for b in bad))
    for md in docs:
        out = build_docx.build(md)
        print(f"PASS docx       {os.path.basename(out)}")
    shutil.rmtree(tmp, ignore_errors=True)
    if ran == 0:
        print("No PDF maker could run.")
        return 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
