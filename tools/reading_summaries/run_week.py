#!/usr/bin/env python3
"""Add the reading summaries of one or more weeks to the DS 501 working decks.

    python tools/reading_summaries/run_week.py 12           # week 12
    python tools/reading_summaries/run_week.py 6 7 8        # several weeks
    python tools/reading_summaries/run_week.py 6 --dry-run  # build the slides only

For each week: check wNN.json, find the "Optional" slide of the deck's Papers to Read
section, build two slides per paper numbered to fit the section, insert them after that
slide and renumber the section (merge_into_weekly.ps1 -NoPdf). The deck is the working
deck "DS 501 · Week N – …" in ../ce_501_ds/slides. A deck that already has summaries is
skipped. Weeks 1-5 were merged earlier, by hand, into the published decks.

Needs Windows with PowerPoint, Node with pptxgenjs (npm install in this folder) and
python-pptx.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml
from pptx import Presentation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT.parent / "ce_501_ds" / "slides"
BUILD = HERE / "build"
C = yaml.safe_load((ROOT / "course.yml").read_text(encoding="utf-8"))


def source_deck(n):
    found = [p for p in SRC.glob("*.pptx") if re.search(rf"Week {n} –", p.name)]
    if len(found) != 1:
        sys.exit(f"week {n}: expected one deck in {SRC}, found {len(found)}")
    return found[0]


def find_optional_slide(deck, n):
    prs = Presentation(str(deck))
    hit = None
    for i, s in enumerate(prs.slides, 1):
        texts = [sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame]
        if any(re.match(rf"WEEK {n} · (REQUIRED|OPTIONAL) READING \d+ ·", t.upper()) for t in texts):
            sys.exit(f"week {n}: {deck.name} already contains reading summaries (slide {i})")
        if any(t.startswith(f"DS 501 · Week {n} · Papers to Read") for t in texts) and "Optional" in texts:
            hit = (i, next((t for t in texts if re.fullmatch(r"\d+ / \d+", t)), None))
    if not hit or not hit[1]:
        sys.exit(f"week {n}: no numbered 'Optional' slide in the Papers to Read section of {deck.name}")
    return hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("weeks", type=int, nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    BUILD.mkdir(exist_ok=True)
    for n in args.weeks:
        js = HERE / f"w{n:02d}.json"
        subprocess.run([sys.executable, str(HERE / "check_summaries.py"), js.name], check=True)
        papers = json.loads(js.read_text(encoding="utf-8"))
        title = next(w["title"] for w in C["weeks"] if w["num"] == n)
        deck = source_deck(n)
        after, counter = find_optional_slide(deck, n)
        k, old_total = map(int, counter.split(" / "))
        out = BUILD / f"w{n:02d}_papers.pptx"
        subprocess.run(["node", str(HERE / "build_readings_deck.js"), str(js), str(n), title, str(out),
                        str(k + 1), str(old_total + 2 * len(papers))], check=True, cwd=HERE)
        print(f"week {n}: {2 * len(papers)} slides after slide {after} ({counter})")
        if args.dry_run:
            continue
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(HERE / "merge_into_weekly.ps1"), "-Weekly", str(deck),
                        "-Summary", str(out), "-After", str(after), "-NoPdf"], check=True)


if __name__ == "__main__":
    main()
