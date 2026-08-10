#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 ai-dictionary-en.json（私有完整版，含英文层）+ ai-dictionary-free.json（线上公开版）
生成 ai-dictionary-free-en.json（公开版英文数据层）。

分层策略（镜像 free.json 的公开切法）：
- 1327 条索引字段全开：id / term / term_zh / entry_type / category / category_en /
  difficulty / difficulty_en / definition_short / definition_short_en / aliases /
  updated_at / displayName / is_sample
- 51 条样板（is_sample=true）额外携带英文深度字段：front_en / back_en /
  definition_long_en / why_it_matters_en / memory_hook_en / example_en / examples_en /
  related_terms / source_links
- 非样板（is_sample=false）的 1276 条绝不携带任何深度字段（en + zh），
  这是「不泄漏完整版」红线，脚本内置断言强制检查。

用法：
  python3 build-free-en-version.py          # dry-run，只跑合并 + 自检，不写文件
  python3 build-free-en-version.py --write  # 实际生成 ai-dictionary-free-en.json
"""

import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

EN_SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-dictionary-en.json")
FREE_SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-dictionary-free.json")
DST = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-dictionary-free-en.json")

# ============================================================
# 字段定义
# ============================================================

# 所有 1327 条都有的索引字段（顺序即输出 key 顺序；_en 后缀从 en.json 取，其余从 free.json 取）
INDEX_FIELDS = [
    "id", "term", "term_zh", "entry_type", "category", "category_en",
    "difficulty", "difficulty_en", "definition_short", "definition_short_en",
    "aliases", "updated_at", "displayName",
]

# 索引层中从 en.json 取值的英文字段
INDEX_FIELDS_EN = {"category_en", "difficulty_en", "definition_short_en"}

# 仅样板卡（is_sample=true）的英文深度字段
DEEP_FIELDS_EN = [
    "front_en", "back_en", "definition_long_en", "why_it_matters_en",
    "memory_hook_en", "example_en", "examples_en",
]

# 语言中性字段（样板卡原样保留）
DEEP_FIELDS_NEUTRAL = ["related_terms", "source_links"]

# 非样板卡禁止出现的深度字段键（en + zh）—— 泄漏红线
FORBIDDEN_DEEP_KEYS = (
    DEEP_FIELDS_EN
    + ["front", "back", "definition_long", "why_it_matters", "memory_hook", "example"]
)

# 目标条数（与 free.json 强一致）
TARGET_TOTAL = 1327


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_terms(free_terms, en_terms):
    """按 id 从 en_terms 取英文层，合并到 free 索引。

    保持 free_terms 顺序；两文件存在重复 id（70 组），按出现顺序逐条消耗匹配，
    保证与位置一一对应。
    """
    en_by_id = defaultdict(deque)
    for t in en_terms:
        en_by_id[t["id"]].append(t)

    out = []
    for ft in free_terms:
        fid = ft["id"]
        if not en_by_id[fid]:
            raise ValueError(f"en.json 中找不到 id={fid} 的对应词条")
        et = en_by_id[fid].popleft()

        entry = {}
        for k in INDEX_FIELDS:
            if k in INDEX_FIELDS_EN:
                v = et.get(k)
                entry[k] = "" if v is None else v
            else:
                entry[k] = ft.get(k)

        is_sample = bool(ft.get("is_sample"))
        entry["is_sample"] = is_sample

        if is_sample:
            for k in DEEP_FIELDS_EN:
                entry[k] = et.get(k)
            for k in DEEP_FIELDS_NEUTRAL:
                v = et.get(k)
                entry[k] = [] if v is None else v

        out.append(entry)
    return out


def run_self_checks(free_data, out_terms):
    """内置自检：全部通过才返回 True，否则抛 AssertionError。"""
    free_terms = free_data["terms"]
    free_samples = [t for t in free_terms if t.get("is_sample")]
    out_samples = [t for t in out_terms if t.get("is_sample")]

    print("\n========== 自检报告 ==========")

    # 1. 总条数
    assert len(out_terms) == TARGET_TOTAL, f"条数不符: {len(out_terms)} != {TARGET_TOTAL}"
    print(f"[1] 总条数: {len(out_terms)} == {TARGET_TOTAL}  ✓")

    # 2. 样板数量（与 free.json 一致）
    assert len(out_samples) == len(free_samples) == 51, (
        f"样板数量不符: out={len(out_samples)} free={len(free_samples)}"
    )
    assert [t["id"] for t in out_samples] == [t["id"] for t in free_samples], "样板 id 顺序与 free.json 不一致"
    print(f"[2] 样板数量: {len(out_samples)} == free.json {len(free_samples)}  ✓")

    # 3. definition_short_en 全覆盖（允许空串，但报告空数量）
    missing_short = [t["id"] for t in out_terms if "definition_short_en" not in t]
    empty_short = [t["id"] for t in out_terms if t.get("definition_short_en") in (None, "")]
    nonempty_short = len(out_terms) - len(empty_short)
    assert not missing_short, f"缺失 definition_short_en: {missing_short}"
    print(f"[3] definition_short_en 键全覆盖 ✓（非空 {nonempty_short} 条 / 空 {len(empty_short)} 条）")

    # 4. 泄漏检查：非样板禁带深度字段；样板深度字段齐全
    leak_ids = []
    for t in out_terms:
        if not t.get("is_sample"):
            bad = [k for k in FORBIDDEN_DEEP_KEYS if k in t]
            if bad:
                leak_ids.append((t["id"], bad))
    assert not leak_ids, f"泄漏：非样板卡携带深度字段 {leak_ids}"
    print(f"[4a] 泄漏检查（非样板 1276 条）: 无任何深度字段键  ✓")

    incomplete = []
    required = DEEP_FIELDS_EN + DEEP_FIELDS_NEUTRAL
    for t in out_samples:
        bad = [k for k in required if k not in t]
        if bad:
            incomplete.append((t["id"], bad))
    assert not incomplete, f"样板卡深度字段不齐全: {incomplete}"
    print(f"[4b] 泄漏检查（样板 {len(out_samples)} 条）: 深度字段全部齐全  ✓")

    # 5. id 集合与 free.json 完全一致
    assert set(t["id"] for t in out_terms) == set(t["id"] for t in free_terms), "id 集合与 free.json 不一致"
    print(f"[5] id 集合与 free.json 完全一致（{len(set(t['id'] for t in out_terms))} 个唯一 id）  ✓")

    # 6. category_en / difficulty_en 全覆盖（报告缺失数；en.json 缺失则允许空串）
    miss_cat = [t["id"] for t in out_terms if "category_en" not in t]
    miss_diff = [t["id"] for t in out_terms if "difficulty_en" not in t]
    empty_cat = [t["id"] for t in out_terms if t.get("category_en") in (None, "")]
    empty_diff = [t["id"] for t in out_terms if t.get("difficulty_en") in (None, "")]
    assert not miss_cat and not miss_diff, f"category_en/difficulty_en 键缺失: cat={miss_cat} diff={miss_diff}"
    print(f"[6] category_en 全覆盖 ✓（空 {len(empty_cat)} 条） / difficulty_en 全覆盖 ✓（空 {len(empty_diff)} 条）")

    # 额外：样板 source_links 默认补空的数量
    defaulted_sl = [t["id"] for t in out_samples if t.get("source_links") == []]
    if defaulted_sl:
        print(f"    备注：en.json 缺失 source_links 的样板卡（已默认补空数组）: {defaulted_sl}")

    print("========== 自检全部通过 ==========\n")
    return {
        "total": len(out_terms),
        "samples": len(out_samples),
        "short_nonempty": nonempty_short,
        "short_empty": len(empty_short),
        "cat_empty": len(empty_cat),
        "diff_empty": len(empty_diff),
        "defaulted_source_links": defaulted_sl,
    }


def build_free_en_version(free_data, en_data, write=False):
    free_terms = free_data["terms"]
    en_terms = en_data["terms"]
    print(f"free.json 词条数: {len(free_terms)} | en.json 词条数: {len(en_terms)}")

    out_terms = build_terms(free_terms, en_terms)
    print(f"合并完成: {len(out_terms)} 条（is_sample 标记保持 free.json 原值）")

    report = run_self_checks(free_data, out_terms)

    if not write:
        print("[dry-run] 未生成文件。加 --write 实际生成。")
        return None

    out_data = {
        "generated_at": "2026-08-11",
        "source_note": "AI 词典公开版英文层 —— 1327 索引英文名/短释义 + 51 样板英文深度字段。英文完整版为私有资产，见 ai-dictionary-en.json。",
        "edition": "public-en",
        "total_terms": len(out_terms),
        "sample_terms": len([t for t in out_terms if t.get("is_sample")]),
        "terms": out_terms,
        "updated_at": "2026-08-11",
    }

    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    size_kb = DST.stat().st_size / 1024
    print(f"[写入] {DST}")
    print(f"  总词条: {len(out_terms)}")
    print(f"  样板词条: {out_data['sample_terms']}")
    print(f"  文件大小: {size_kb:.1f} KB ({size_kb / 1024:.2f} MB)")

    print("\n---------- 汇总 ----------")
    print(f"  非空 definition_short_en: {report['short_nonempty']} 条（空 {report['short_empty']} 条）")
    print(f"  category_en 缺失: {report['cat_empty']} 条（均为空串）")
    print(f"  difficulty_en 缺失: {report['diff_empty']} 条（均为空串）")
    print(f"  source_links 默认补空: {len(report['defaulted_source_links'])} 条")
    return out_data


def main():
    write = "--write" in sys.argv
    free_data = load_json(FREE_SRC)
    en_data = load_json(EN_SRC)
    build_free_en_version(free_data, en_data, write=write)


if __name__ == "__main__":
    main()
