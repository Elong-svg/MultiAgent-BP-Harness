#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 SKILL.md 到 v3.1 版本
- 更新 Claw 职责（增加格式排版、模板应用、格式审核）
- 更新禁止行为
- 更新特殊权限
"""

import os

skill_md_path = r"C:\Users\吴传奇\.workbuddy\skills\business-plan-creator\SKILL.md"

# 读取文件
with open(skill_md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 Claw 的职责描述（表格行）
old_line = "| **Claw（项目总监）** | 数据收集 + 进度监控 + 质量把关 + 增量整合 | finance-data-retrieval, Word/PDF 文档生成 | Excel 文件处理，金融财务分析整合包 | ❌ 自己写 Python 爬数据 | **一票否决权**（进度/资源/交付） |"
new_line = "| **Claw（项目总监）** | 数据收集 + 进度监控 + **格式排版 + 模板应用 + 格式审核** + 质量把关 + 增量整合 | finance-data-retrieval, Word/PDF 文档生成 | Excel 文件处理，金融财务分析整合包 | ❌ 自己写 Python 爬数据<br>❌ 手打目录<br>❌ 手动排版 | **一票否决权**（进度/资源/交付/**格式**） |"

if old_line in content:
    content = content.replace(old_line, new_line)
    print("✅ 已更新 Claw 职责描述")
else:
    print("❌ 未找到旧版 Claw 职责描述")
    print("搜索内容：", repr(old_line[:50]))

# 写回文件
with open(skill_md_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ SKILL.md v3.1 更新完成")
