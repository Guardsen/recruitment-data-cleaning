# -*- coding: utf-8 -*-
"""【需求 3】统计与导出：第一志愿人数汇总表、志愿填写情况统计、导出干净数据。"""
import csv
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import COLUMNS, read_rows, validate_all

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "data", "sample_applications.csv")
OUT_DIR = os.path.join(HERE, "output")
SUMMARY_PATH = os.path.join(OUT_DIR, "first_choice_summary.csv")
CLEAN_PATH = os.path.join(OUT_DIR, "cleaned.csv")


def main(path):
    _, rows = read_rows(path)
    clean = [row for row, reasons in validate_all(rows) if not reasons]

    counter = Counter(r.get("志愿1", "") or "（未填）" for r in clean)
    both = sum(1 for r in clean if r.get("志愿1", "") and r.get("志愿2", ""))
    only_one = sum(
        1 for r in clean if bool(r.get("志愿1", "")) != bool(r.get("志愿2", ""))
    )
    neither = sum(1 for r in clean if not r.get("志愿1", "") and not r.get("志愿2", ""))

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(SUMMARY_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["志愿1", "人数"])
        for name, n in counter.most_common():
            writer.writerow([name, n])
    with open(CLEAN_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for r in clean:
            writer.writerow([r.get(c, "") for c in COLUMNS])

    print("== 需求 3：统计与导出 ==")
    print("干净数据行数：%d（已剔除问题行）" % len(clean))
    print("按第一志愿分组的人数汇总表：")
    for name, n in counter.most_common():
        print("  %s：%d" % (name, n))
    print(
        "两个志愿都填了：%d 人；只填了一个：%d 人；两个都没填：%d 人"
        % (both, only_one, neither)
    )
    print("汇总表已导出：%s" % SUMMARY_PATH)
    print("干净数据已导出：%s" % CLEAN_PATH)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
