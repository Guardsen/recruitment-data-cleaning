# -*- coding: utf-8 -*-
"""共享的读取与校验规则（需求 2、需求 3 共用）。

所有边界情况的假设集中记录在 README.md 的「假设（边界情况）」一节。
"""
import csv

COLUMNS = ["姓名", "学号", "邮箱", "志愿1", "志愿2", "推荐人"]
EMAIL_DOMAIN = "smbu.edu.cn"


def is_blank(value):
    """空值 = None、空字符串或纯空白字符串。"""
    return value is None or str(value).strip() == ""


def read_rows(path):
    """读取报名表 CSV。

    返回 (fieldnames, rows)：
    - fieldnames：表头列表；
    - rows：dict 列表，六个业务列的值已去掉首尾空白，
      并附加 _row_no 键 = 文件物理行号（表头为第 1 行，首条数据为第 2 行）。
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [(c or "").strip() for c in (reader.fieldnames or [])]
        rows = []
        for row_no, raw in enumerate(reader, start=2):
            row = {
                (k or "").strip(): (v or "").strip()
                for k, v in raw.items()
                if k is not None
            }
            row["_row_no"] = row_no
            rows.append(row)
    return fieldnames, rows


def validate_row(row):
    """单行校验（需求 2 的规则 1、2）。返回问题原因列表，空列表表示该行无问题。"""
    reasons = []
    sid = row.get("学号", "")
    email = row.get("邮箱", "")
    if sid == "":
        reasons.append("学号为空（不是纯数字）")
    elif not (sid.isascii() and sid.isdigit()):
        reasons.append("学号不是纯数字：%s" % sid)
    if email == "":
        reasons.append("邮箱为空")
    elif sid and email.lower() != ("%s@%s" % (sid, EMAIL_DOMAIN)).lower():
        reasons.append(
            "邮箱与学号不匹配：应为 %s@%s，实际为 %s" % (sid, EMAIL_DOMAIN, email)
        )
    return reasons


def validate_all(rows):
    """全量校验（单行规则 + 重复报名规则）。

    重复报名 = 同一学号出现两次及以上：保留第一次出现，第二次及之后判为问题行。
    返回 [(row, reasons), ...]，顺序与输入一致。
    """
    first_row = {}
    total = {}
    for row in rows:
        sid = row.get("学号", "")
        if sid:
            total[sid] = total.get(sid, 0) + 1
            first_row.setdefault(sid, row["_row_no"])

    results = []
    running = {}
    for row in rows:
        reasons = validate_row(row)
        sid = row.get("学号", "")
        if sid:
            running[sid] = running.get(sid, 0) + 1
            if running[sid] > 1:
                reasons.append(
                    "重复报名：学号 %s 共出现 %d 次，此为第 %d 次（保留第 %d 行的首次报名）"
                    % (sid, total[sid], running[sid], first_row[sid])
                )
        results.append((row, reasons))
    return results
