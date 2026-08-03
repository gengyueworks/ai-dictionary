#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 ai-dictionary.json 生成 ai-dictionary-free.json（公开版数据）。

分层策略（深度切）：
- 1327 条索引字段全开（term / term_zh / entry_type / category / difficulty / definition_short / aliases / updated_at / displayName）
- 50 条精选额外带完整字段 + is_sample: true（样板间）
- 给中文名精选词条补英文 aliases，让英文搜索也能命中

用法：
  python3 build-free-version.py          # dry-run，只验证精选清单
  python3 build-free-version.py --write  # 实际生成 free.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-dictionary.json")
DST = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-dictionary-free.json")

# ============================================================
# 精选 50 条：按 entry_type 加权 + 头部价值人工挑选 + 去重
# ============================================================
SAMPLE_TERMS = {
    "concept": [
        "Agent", "Transformer 架构", "RAG vs Fine-tune Decision Matrix", "图灵测试",
        "CNN vs Transformer", "Multimodal LLM", "LLM-as-Judge",
        "Open-Source LLM", "Reinforcement Learning Basics", "Autoencoder",
        "Heuristic Search", "NLP 简史", "Production Systems",
        "Cross-Attention", "规则系统", "AI 安全",
        "Sparse Attention", "AI 商业化",
    ],
    "person": [
        "艾伦·图灵", "杰弗里·辛顿", "山姆·奥特曼", "达里奥·阿莫迪",
        "安德烈·卡帕西", "黄仁勋", "梁文锋", "李飞飞",
        "德米斯·哈萨比斯", "约书亚·本吉奥",
    ],
    "model": [
        "GPT", "Claude", "Gemini", "Llama", "Sora",
        "Stable Diffusion 图像生成模型", "CLIP", "GPT-4V",
    ],
    "product": [
        "ChatGPT", "Cursor", "Siri", "LangChain", "Midjourney", "AutoGPT",
    ],
    "company": [
        "Anthropic", "Hugging Face", "苹果", "波士顿动力",
    ],
    "paper": [
        "Attention Is All You Need", "GPT 系列论文",
    ],
    "system": [
        "AlphaFold", "ELIZA 聊天程序",
    ],
}

# ============================================================
# 英文 aliases 映射（给中文名精选词条补，让英文搜索命中）
# ============================================================
EN_ALIASES = {
    "艾伦·图灵": "Alan Turing",
    "杰弗里·辛顿": "Geoffrey Hinton",
    "山姆·奥特曼": "Sam Altman",
    "达里奥·阿莫迪": "Dario Amodei",
    "安德烈·卡帕西": "Andrej Karpathy",
    "黄仁勋": "Jensen Huang",
    "梁文锋": "Liang Wenfeng",
    "李飞飞": "Fei-Fei Li",
    "德米斯·哈萨比斯": "Demis Hassabis",
    "约书亚·本吉奥": "Yoshua Bengio",
    "伊利亚·苏茨克维": "Ilya Sutskever",
    "吴恩达": "Andrew Ng",
    "杨立昆": "Yann LeCun",
    "罗德尼·布鲁克斯": "Rodney Brooks",
    "艾伦·纽厄尔": "Allen Newell",
    "马文·明斯基": "Marvin Minsky",
    "约翰·麦卡锡": "John McCarthy",
    "克劳德·香农": "Claude Shannon",
    "约翰·冯·诺依曼": "John von Neumann",
    "雷·库兹韦尔": "Ray Kurzweil",
}

# ============================================================
# 索引卡保留字段（免费版所有词条都有）
# ============================================================
INDEX_FIELDS = [
    "id", "term", "term_zh", "entry_type", "category", "difficulty",
    "definition_short", "aliases", "updated_at", "displayName",
]

# ============================================================
# 精选卡额外完整字段（仅 is_sample=True 的 50 条）
# ============================================================
FULL_FIELDS = [
    "front", "back", "definition_long", "example",
    "why_it_matters", "memory_hook", "related_terms", "source_links",
]


def load_source():
    with SRC.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_term(terms, name):
    """按 term 字段精确匹配（大小写不敏感）"""
    for t in terms:
        if t.get("term", "").strip().lower() == name.strip().lower():
            return t
    return None


def verify_samples(terms):
    """验证精选清单，返回 (found, missing)"""
    found = {}
    missing = []
    for etype, names in SAMPLE_TERMS.items():
        for name in names:
            t = find_term(terms, name)
            if t:
                found[t.get("term", "")] = t
            else:
                missing.append((etype, name))
    return found, missing


def build_free_version(data, write=False):
    terms = data.get("terms", [])
    print(f"源词条数: {len(terms)}")

    found, missing = verify_samples(terms)
    print(f"\n精选匹配: {len(found)} / {sum(len(v) for v in SAMPLE_TERMS.values())}")

    if missing:
        print("\n[警告] 以下精选词未找到，请检查 term 字段：")
        for etype, name in missing:
            print(f"  [{etype}] {name}")

    if not write:
        print("\n[dry-run] 未生成文件。加 --write 实际生成。")
        print("\n精选清单（按 entry_type）：")
        for etype, names in SAMPLE_TERMS.items():
            print(f"\n  [{etype}] {len(names)} 条")
            for name in names:
                t = find_term(terms, name)
                if t:
                    zh = t.get("term_zh", "") or ""
                    cat = t.get("category", "") or ""
                    print(f"    ✓ {t.get('term',''):30s} | {zh:20s} | {cat}")
                else:
                    print(f"    ✗ {name} (未找到)")
        return None

    # 构建免费版 terms
    free_terms = []
    sample_count = 0
    for t in terms:
        term_name = t.get("term", "")
        is_sample = term_name in found

        # 索引字段（所有词条）
        entry = {k: t.get(k) for k in INDEX_FIELDS}

        # 精选词条补完整字段 + 标记 + 英文 aliases
        if is_sample:
            entry["is_sample"] = True
            for f in FULL_FIELDS:
                entry[f] = t.get(f)

            # 补英文 aliases
            existing_aliases = list(t.get("aliases", []) or [])
            en_alias = EN_ALIASES.get(term_name)
            if en_alias and en_alias not in existing_aliases:
                existing_aliases.append(en_alias)
            entry["aliases"] = existing_aliases
            sample_count += 1
        else:
            entry["is_sample"] = False

        free_terms.append(entry)

    free_data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_note": "AI 词典公开版（深度切分层）—— 1327 条索引全开 + 50 条精选完整卡。完整版含 why_it_matters / memory_hook 等深度字段。",
        "edition": "public",
        "total_terms": len(free_terms),
        "sample_terms": sample_count,
        "terms": free_terms,
        "updated_at": data.get("updated_at", ""),
    }

    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8") as f:
        json.dump(free_data, f, ensure_ascii=False, indent=2)

    size_kb = DST.stat().st_size / 1024
    print(f"\n[写入] {DST}")
    print(f"  总词条: {len(free_terms)}")
    print(f"  精选词条: {sample_count}")
    print(f"  文件大小: {size_kb:.1f} KB")
    print(f"  完整版大小对比: {SRC.stat().st_size / 1024 / 1024:.1f} MB → {size_kb / 1024:.2f} MB")

    return free_data


def main():
    write = "--write" in sys.argv
    data = load_source()
    build_free_version(data, write=write)


if __name__ == "__main__":
    main()
