#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改造 timeline HTML 为公开版，并在词典页面加回时间轴链接。

改造点：
1. timeline fetch → ai-timeline-data-free.json
2. timeline loadDictionary → ai-dictionary-free.json
3. timeline loadReviewTerms → return []（不加载评审草稿）
4. timeline 深度字段渲染 → renderLockedBlock（遮罩）
5. timeline topbar 加"词典"链接
6. timeline CSS 加遮罩样式
7. 词典 lab.html 加回"时间轴"链接
"""

from pathlib import Path

TIMELINE_SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-timeline-design-fixed.html")
TIMELINE_DST = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-timeline-design-fixed.html")
DICT_HTML = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-dictionary-lab.html")


def patch_timeline():
    html = TIMELINE_SRC.read_text(encoding="utf-8")

    # 1. timeline fetch → ai-timeline-data-free.json
    old = 'const data = await loadJSON("ai-timeline-data.json");'
    new = 'const data = await loadJSON("ai-timeline-data-free.json");'
    assert old in html, "timeline fetch 旧路径未找到"
    html = html.replace(old, new)
    print("[1/7] timeline fetch -> ai-timeline-data-free.json")

    # 2. loadDictionary → ai-dictionary-free.json
    old = 'const data = await loadJSON("ai-dictionary.json");'
    new = 'const data = await loadJSON("ai-dictionary-free.json");'
    assert old in html, "dictionary fetch 旧路径未找到"
    html = html.replace(old, new)
    print("[2/7] loadDictionary -> ai-dictionary-free.json")

    # 3. loadReviewTerms → return []
    old = '''    async function loadReviewTerms() {
      try {
        const data = await loadJSON("ai-dictionary-expansion-review-draft.json");
        return (data.items || []).filter(term => term && term.term);
      } catch (error) {
        return [];
      }
    }'''
    new = '''    async function loadReviewTerms() {
      // 公开版不加载评审草稿
      return [];
    }'''
    assert old in html, "loadReviewTerms 旧结构未找到"
    html = html.replace(old, new)
    print("[3/7] loadReviewTerms -> return []（评审草稿不上架）")

    # 4. 深度字段渲染 → renderLockedBlock（只替换表达式，不管缩进）
    html = html.replace(
        '${renderDetailBlock("背后现场", event.story)}',
        '${renderLockedBlock("背后现场")}',
    ).replace(
        '${renderDetailBlock("为何重要", cleanWhy(event.why))}',
        '${renderLockedBlock("为何重要")}',
    )
    assert "renderLockedBlock" in html, "renderLockedBlock 替换失败"
    print("[4/7] 深度字段渲染 -> renderLockedBlock（遮罩）")

    # 5. 新增 renderLockedBlock 函数（插入到 renderDetailBlock 前）
    new_func = '''    function renderLockedBlock(label) {
      return `
        <div class="detail-locked">
          <p class="detail-label">${escapeHTML(label)}</p>
          <div class="locked-body">
            <p class="detail-text">这是完整版深度内容。</p>
            <p class="detail-text">开放查阅版仅展示事件摘要，完整版含背后现场、为何重要等原创深度字段。</p>
          </div>
          <div class="locked-veil" aria-hidden="true"></div>
        </div>
      `;
    }

'''
    marker = "    function renderDetailBlock(label, text) {"
    assert marker in html, "renderDetailBlock 函数未找到"
    html = html.replace(marker, new_func + marker)
    print("[5/7] 已插入 renderLockedBlock 函数")

    # 6. topbar 加"词典"链接
    old = '''        <span class="translate-mini" aria-label="辅助翻译">'''
    new = '''        <a class="chip dict-link" href="ai-dictionary-lab.html" title="进入 AI 词典">词典 →</a>
        <span class="translate-mini" aria-label="辅助翻译">'''
    assert old in html, "translate-mini 未找到"
    html = html.replace(old, new)
    print("[6/7] topbar 加词典链接")

    # 7. CSS 加遮罩 + 词典链接样式
    new_css = '''
    /* ===== 公开版分层样式 ===== */
    .dict-link {
      border: 1px solid var(--blue);
      color: var(--paper-2);
      background: var(--blue);
      font-weight: 800;
      text-decoration: none;
    }
    .dict-link:hover { text-decoration: none; opacity: 0.9; }

    .detail-locked {
      position: relative;
      overflow: hidden;
      min-height: 90px;
      padding: 12px 0;
    }
    .detail-locked .locked-body {
      filter: blur(4px);
      opacity: 0.5;
      user-select: none;
      pointer-events: none;
    }
    .detail-locked .locked-veil {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, transparent 0%, rgba(243, 239, 228, 0.4) 30%, rgba(243, 239, 228, 0.92) 70%);
      pointer-events: none;
    }
    '''
    html = html.replace("  </style>", new_css + "  </style>")
    print("[7/7] CSS 加遮罩 + 词典链接样式")

    TIMELINE_DST.write_text(html, encoding="utf-8")
    print(f"\n[写入] {TIMELINE_DST} ({TIMELINE_DST.stat().st_size / 1024:.1f} KB)")


def patch_dict_link():
    """在词典 lab.html 加回时间轴链接"""
    html = DICT_HTML.read_text(encoding="utf-8")

    old = '''        <span class="pill" id="nav-count">读取中</span>
        <a class="pill full-version-cta" id="full-version-link" href="#" title="解锁全部深度内容">完整版 →</a>'''
    new = '''        <a class="pill" href="ai-timeline-design-fixed.html" title="进入 AI 时间轴">← 时间轴</a>
        <span class="pill" id="nav-count">读取中</span>
        <a class="pill full-version-cta" id="full-version-link" href="#" title="解锁全部深度内容">完整版 →</a>'''
    assert old in html, "词典 nav-stats 结构未找到"
    html = html.replace(old, new)

    DICT_HTML.write_text(html, encoding="utf-8")
    print(f"[写入] {DICT_HTML}（加回时间轴链接）")


if __name__ == "__main__":
    print("=== 改造 timeline HTML ===")
    patch_timeline()
    print("\n=== 词典加回时间轴链接 ===")
    patch_dict_link()
