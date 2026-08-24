#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 ai-timeline-data.json 生成 ai-timeline-data-free.json（公开版时间轴数据）。

分层策略（字段级分层）：
- 保留：year / date / title_zh / title_en / type / importance / summary_zh / related_terms / tags / source_name / source_url / confidence
- 砍掉：why_it_matters_zh / behind_scenes_zh / learning_path_hint（深度字段，完整版才有）

完整时间线全开（252 个事件不残缺），深度内容做遮罩。
"""

import json
from pathlib import Path

SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/30-项目-网站/AI时间轴/_私有数据/ai-timeline-data-263条-完整版.json")
DST = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-timeline-data-free.json")

# 深度字段（砍掉）
DEEP_FIELDS = ["why_it_matters_zh", "behind_scenes_zh", "learning_path_hint"]


def main():
    with SRC.open("r", encoding="utf-8") as f:
        data = json.load(f)

    src_size = SRC.stat().st_size / 1024

    # 砍掉 timeline 数组的深度字段
    timeline = data.get("timeline", [])
    for event in timeline:
        for field in DEEP_FIELDS:
            event.pop(field, None)

    # events 数组也砍（虽然主用的是 timeline）
    events = data.get("events", [])
    for event in events:
        for field in DEEP_FIELDS:
            event.pop(field, None)
    # timeline 数组缺英文摘要时，从 events 数组按 (date, title_zh) 回填
    EN_FIELDS = ["summary_en", "card_summary_en", "why_it_matters_en", "behind_scenes_en"]
    en_lookup = {
        (e.get("date"), e.get("title_zh")): e
        for e in events
        if any(e.get(f) for f in EN_FIELDS)
    }
    filled = 0
    for event in timeline:
        src = en_lookup.get((event.get("date"), event.get("title_zh")))
        if not src:
            continue
        for f in EN_FIELDS:
            if not event.get(f) and src.get(f):
                event[f] = src[f]
                filled += 1
    print(f"  timeline 回填英文字段: {filled} 处")

    # 标记版本
    data["edition"] = "public"
    data["source_note"] = "AI 时间轴公开版 —— 265 个事件全开，深度字段（为何重要 / 背后现场 / 学习路径）在完整版。"

    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    dst_size = DST.stat().st_size / 1024
    print(f"[写入] {DST}")
    print(f"  事件数: {len(timeline)}（timeline）+ {len(events)}（events）")
    print(f"  砍掉字段: {', '.join(DEEP_FIELDS)}")
    print(f"  文件大小: {src_size:.1f} KB → {dst_size:.1f} KB（压缩 {(1 - dst_size/src_size)*100:.0f}%）")


if __name__ == "__main__":
    main()
