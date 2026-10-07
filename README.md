# 招新报名数据清洗与统计工具

处理协会招新报名表（问卷导出的 CSV）的小工具：不改动原文件，输出问题清单、汇总表和清洗后的干净数据。
纯 Python 标准库实现，无需安装任何第三方依赖。

## 目录结构

```
.
├── README.md
├── rules.py                      # 共享的读取与校验规则（需求 2 引入，需求 3 复用）
├── step1_overview.py             # 需求 1：读入与概览
├── step2_validate.py             # 需求 2：校验与清洗 → output/problem_list.csv
├── step3_stats.py                # 需求 3：统计与导出 → output/first_choice_summary.csv、output/cleaned.csv
├── data/
│   └── sample_applications.csv   # 样例报名数据（内置各种边界情况，可换成真实报名表）
└── output/                       # 运行产物（已 gitignore）
```

## 怎么跑

环境：Python 3.7 及以上，无需安装第三方包。

```bash
python step1_overview.py 你的报名表.csv
python step2_validate.py 你的报名表.csv
python step3_stats.py  你的报名表.csv
```

不带参数时默认处理自带的 `data/sample_applications.csv`。三个脚本相互独立，可以只跑其中一个。

## 三个需求分别做了什么

- **需求 1（step1_overview.py）**：打印一共多少行（不含表头）、每列有多少个空值、有没有完全重复的行（给出重复行号）。
- **需求 2（step2_validate.py）**：校验「学号必须是纯数字」「邮箱必须是 学号@smbu.edu.cn」「同一学号出现两次即重复报名」；有问题的行连同原因导出到 `output/problem_list.csv`，**原文件一个字都不改**。
- **需求 3（step3_stats.py）**：按第一志愿分组统计人数，汇总表存 `output/first_choice_summary.csv`；统计两个志愿都填了 / 只填一个 / 都没填的人数；把剔除问题行后的干净数据导出为 `output/cleaned.csv`。

## 假设（边界情况）

1. 需求没说明学号位数，因此只校验「纯数字（ASCII 数字）」，不限制位数。
2. 「空值」= 空字符串或纯空白字符串；读入时统一去掉首尾空白，导出的干净数据也是去空白后的值。
3. 邮箱与「学号@smbu.edu.cn」的比较不区分大小写。
4. 学号为空、邮箱为空本身即判为校验不通过（无法满足「纯数字」「必须是 学号@smbu.edu.cn」）。
5. 重复报名保留第一次出现的行（按文件顺序），第二次及之后的行判为问题行。
6. 完全重复的行必然同学号，因此也会按重复报名在清洗时剔除；需求 1 只报告不处理。
7. 需求 3 的统计基于干净数据（剔除问题行后）；志愿1 为空的行在汇总表里计入「（未填）」组。
8. 问题清单里的「行号」= CSV 文件物理行号（表头是第 1 行，首条数据是第 2 行），方便在 Excel 里对照。
9. 输入按 UTF-8 读取（兼容带 BOM）；所有输出用带 BOM 的 UTF-8，Excel 双击打开中文不乱码。
10. 输入缺列时按空值处理，多出的列忽略（只处理姓名、学号、邮箱、志愿1、志愿2、推荐人六列）。

## 提交方式（GitHub + 3 次 PR）

本地 git 已按「一次 PR 对应一个需求」组织成堆叠分支：

| 分支 | 相对 main 新增的内容 |
| --- | --- |
| `main` | README、样例数据、.gitignore |
| `req1-overview` | `step1_overview.py` |
| `req2-validate` | `rules.py`、`step2_validate.py` |
| `req3-stats` | `step3_stats.py` |

把仓库推到自己的 GitHub 后，按 `req1-overview` → `req2-validate` → `req3-stats` 的顺序依次创建并合并 PR，每个 PR 的 diff 恰好对应一个需求。
