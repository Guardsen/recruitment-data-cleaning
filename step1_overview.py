# -*- coding: utf-8 -*-
"""【需求 1】读入与概览：总行数、每列空值数、完全重复的行。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules import COLUMNS, is_blank, read_rows

DEFAULT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "sample_applications.csv"
)


def main(path):
    _, rows = read_rows(path)
    print("== 需求 1：读入与概览 ==")
    print("文件：%s" % path)
    print("一共多少行：%d（不含表头）" % len(rows))

    print("每列空值数：")
    for col in COLUMNS:
        print("  %s：%d" % (col, sum(1 for r in rows if is_blank(r.get(col)))))

    groups = {}
    for r in rows:
        key = tuple(r.get(c, "") for c in COLUMNS)
        groups.setdefault(key, []).append(r["_row_no"])
    dups = [nos for nos in groups.values() if len(nos) > 1]
    if dups:
        extra = sum(len(nos) - 1 for nos in dups)
        print("有没有完全重复的行：有，%d 组，除首次出现外多出 %d 行" % (len(dups), extra))
        for nos in dups:
            print("  第 %s 行互为完全重复" % "、".join(str(n) for n in nos))
    else:
        print("有没有完全重复的行：没有")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
