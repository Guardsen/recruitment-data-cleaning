# -*- coding: utf-8 -*-
"""【需求 2】校验与清洗：不改原文件，问题行单独导出「问题清单」并写明原因。"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import COLUMNS, read_rows, validate_all

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "data", "sample_applications.csv")
OUT_PATH = os.path.join(HERE, "output", "problem_list.csv")


def main(path):
    _, rows = read_rows(path)
    problems = [(row, reasons) for row, reasons in validate_all(rows) if reasons]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["行号"] + COLUMNS + ["问题原因"])
        for row, reasons in problems:
            writer.writerow(
                [row["_row_no"]] + [row.get(c, "") for c in COLUMNS] + ["；".join(reasons)]
            )

    print("== 需求 2：校验与清洗 ==")
    print("共检查 %d 行，其中问题行 %d 行；原文件未做任何修改" % (len(rows), len(problems)))
    print("问题清单已导出：%s" % OUT_PATH)
    for row, reasons in problems:
        print("  第 %d 行：%s" % (row["_row_no"], "；".join(reasons)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
