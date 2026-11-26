"""Rebuild every unit's Student Notes, Answer Key and Lesson Plan into ../output/."""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_lesson_plan  # noqa: E402
import build_worksheet  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    only = sys.argv[1:]  # optional unit numbers
    for path in sorted(glob.glob(os.path.join(ROOT, "units", "unit*", "content.json"))):
        unit = os.path.basename(os.path.dirname(path)).replace("unit", "")
        if only and unit not in only:
            continue
        for p in build_worksheet.build_unit(path, os.path.join(ROOT, "output", "worksheets")):
            print(os.path.relpath(p, ROOT))
        for p in build_lesson_plan.build(path, os.path.join(ROOT, "output", "lesson-plans")):
            print(os.path.relpath(p, ROOT))
