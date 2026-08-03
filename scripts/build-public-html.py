#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从源头 ai-dictionary-lab.html 改造出公开版 ai-dictionary-lab.html。

改造点：
1. fetch 路径 → ai-dictionary-free.json
2. 顶部导航：删"回时间轴"链接，加"完整版"CTA
3. renderDetail：非 is_sample 词条的深度字段渲染模糊遮罩 + CTA
4. CSS 新增：角标 / 遮罩 / CTA 样式
5. 新增函数：renderLockedSection / renderUpgradeCard
"""

from pathlib import Path

SRC = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-dictionary-lab.html")
DST = Path("/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/gengyueworks-Github/ai-dictionary/ai-dictionary-lab.html")


def main():
    html = SRC.read_text(encoding="utf-8")
    original_len = len(html)

    # ============================================================
    # 改造 1：fetch 路径
    # ============================================================
    html = html.replace(
        "const response = await fetch(`ai-dictionary.json?t=${Date.now()}`);",
        "const response = await fetch(`ai-dictionary-free.json?t=${Date.now()}`);",
    )
    html = html.replace(
        'if (!response.ok) throw new Error("无法读取 ai-dictionary.json。");',
        'if (!response.ok) throw new Error("无法读取 ai-dictionary-free.json。");',
    )
    print("[1/5] fetch 路径已改")

    # ============================================================
    # 改造 2：顶部导航 —— 删"回时间轴"，加"完整版"CTA
    # ============================================================
    old_nav = '''        <a class="pill back-link" id="back-timeline" href="ai-timeline-design.html">← 回时间轴</a>
        <span class="pill" id="nav-count">读取中</span>'''
    new_nav = '''        <span class="pill" id="nav-count">读取中</span>
        <a class="pill full-version-cta" id="full-version-link" href="#" title="解锁全部深度内容">完整版 →</a>'''
    assert old_nav in html, "导航旧结构未找到"
    html = html.replace(old_nav, new_nav)
    print("[2/5] 顶部导航已改（删回时间轴 + 加完整版 CTA）")

    # ============================================================
    # 改造 3：renderDetail —— 加 is_sample 判断 + 锁定遮罩
    # ============================================================
    old_detail = '''      const related = term.related_terms || [];
      const relatedPeople = term.related_people || [];
      const definition = term.definition_short || term.back || "";
      const extended = term.definition_long && term.definition_long !== definition ? term.definition_long : "";
      document.getElementById("entry-status").textContent = termStatus(term);
      const entryMeta = metaLabels(term).map(label => escapeHTML(label)).join(" · ");
      detail.innerHTML = `
        <div class="entry-head">
          <h3>${escapeHTML(term.displayName || term.term)}</h3>
          <p class="entry-kicker">${entryMeta}</p>
        </div>
        ${renderReadCard("一句释义", definition, { primary: true, takeaway: true, maxParts: 1 })}
        ${extended ? renderReadCard("展开理解", extended, { maxParts: 5, collapsible: true }) : ""}
        ${term.why_it_matters ? renderReadCard("为何重要", term.why_it_matters, { maxParts: 2 }) : ""}
        ${term.memory_hook ? renderReadCard("记忆锚点", term.memory_hook, { maxParts: 1 }) : ""}
        ${renderRelatedSection("相关人物", relatedPeople)}
        ${renderRelatedSection("相关卡片", related)}
      `;'''

    new_detail = '''      const related = term.related_terms || [];
      const relatedPeople = term.related_people || [];
      const definition = term.definition_short || term.back || "";
      const extended = term.definition_long && term.definition_long !== definition ? term.definition_long : "";
      const isSample = term.is_sample === true;
      document.getElementById("entry-status").textContent = termStatus(term);
      const entryMeta = metaLabels(term).map(label => escapeHTML(label)).join(" · ");
      const sampleBadge = isSample
        ? '<span class="edition-badge sample">精选样板</span>'
        : '<span class="edition-badge free">开放查阅</span>';
      detail.innerHTML = `
        <div class="entry-head">
          <h3>${escapeHTML(term.displayName || term.term)}</h3>
          <p class="entry-kicker">${entryMeta}</p>
          ${sampleBadge}
        </div>
        ${renderReadCard("一句释义", definition, { primary: true, takeaway: true, maxParts: 1 })}
        ${isSample && extended ? renderReadCard("展开理解", extended, { maxParts: 5, collapsible: true }) : ""}
        ${isSample && term.why_it_matters ? renderReadCard("为何重要", term.why_it_matters, { maxParts: 2 }) : renderLockedSection("为何重要")}
        ${isSample && term.memory_hook ? renderReadCard("记忆锚点", term.memory_hook, { maxParts: 1 }) : renderLockedSection("记忆锚点")}
        ${renderRelatedSection("相关人物", relatedPeople)}
        ${renderRelatedSection("相关卡片", related)}
        ${isSample ? "" : renderUpgradeCard()}
      `;'''

    assert old_detail in html, "renderDetail 旧结构未找到"
    html = html.replace(old_detail, new_detail)
    print("[3/5] renderDetail 已改（加 is_sample 判断 + 锁定遮罩）")

    # ============================================================
    # 改造 4：新增 renderLockedSection / renderUpgradeCard 函数
    # 插入到 renderRelatedSection 函数之后
    # ============================================================
    new_functions = '''
    function renderLockedSection(label) {
      return `
        <section class="read-card locked-section">
          <p class="section-label">${escapeHTML(label)}</p>
          <div class="locked-body">
            <p class="locked-text">这是完整版深度内容。</p>
            <p class="locked-text">开放查阅版仅展示一句释义，完整版含展开理解、为何重要、记忆锚点等原创深度字段。</p>
            <p class="locked-text">—— 升级完整版阅读全部 1327 条深度卡 ——</p>
          </div>
          <div class="locked-veil" aria-hidden="true"></div>
        </section>
      `;
    }

    function renderUpgradeCard() {
      return `
        <section class="read-card upgrade-card">
          <p class="section-label">完整版解锁</p>
          <p class="upgrade-title">这条词条的深度内容，只在完整版。</p>
          <p class="upgrade-detail">完整版含 1327 条词条的展开理解、为何重要、记忆锚点、相关卡片等深度字段，月更新增。</p>
          <a class="upgrade-button" href="#" onclick="window.open('https://github.com/your-username/ai-dictionary', '_blank'); return false;">了解完整版 →</a>
        </section>
      `;
    }
'''
    # 插入到 renderRelatedSection 函数结束后（在 searchLabels 函数前）
    marker = "    function searchLabels(term) {"
    assert marker in html, "searchLabels 函数未找到，无法插入新函数"
    html = html.replace(marker, new_functions + marker)
    print("[4/5] 已插入 renderLockedSection / renderUpgradeCard 函数")

    # ============================================================
    # 改造 5：CSS 新增 —— 角标 / 遮罩 / CTA 样式
    # 插入到 </style> 前
    # ============================================================
    new_css = '''
    /* ===== 公开版分层样式 ===== */
    .full-version-cta {
      border-color: var(--blue);
      color: var(--paper-2);
      background: var(--blue);
      font-weight: 800;
      box-shadow: 3px 3px 0 var(--ink);
      text-decoration: none;
    }
    .full-version-cta:hover { text-decoration: none; transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--ink); }

    .edition-badge {
      display: inline-block;
      margin-top: 8px;
      padding: 3px 10px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.04em;
      border-radius: 999px;
      border: 1px solid var(--ink);
    }
    .edition-badge.sample {
      color: var(--paper-2);
      background: var(--green);
      border-color: var(--green);
    }
    .edition-badge.free {
      color: var(--muted);
      background: rgba(255, 250, 240, 0.6);
    }

    .locked-section {
      position: relative;
      overflow: hidden;
      min-height: 110px;
    }
    .locked-body {
      filter: blur(4px);
      opacity: 0.5;
      user-select: none;
      pointer-events: none;
    }
    .locked-text {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.7;
      margin: 0 0 6px;
    }
    .locked-veil {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, transparent 0%, rgba(243, 239, 228, 0.4) 30%, rgba(243, 239, 228, 0.92) 70%);
      pointer-events: none;
    }

    .upgrade-card {
      border: 2px dashed var(--blue);
      background: rgba(0, 47, 167, 0.04);
      text-align: center;
      padding: 22px 18px;
    }
    .upgrade-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--ink);
      margin: 0 0 8px;
    }
    .upgrade-detail {
      font-size: 13px;
      color: var(--muted);
      line-height: 1.7;
      margin: 0 0 14px;
    }
    .upgrade-button {
      display: inline-block;
      padding: 10px 22px;
      background: var(--blue);
      color: var(--paper-2);
      font-weight: 800;
      border: 2px solid var(--ink);
      box-shadow: 3px 3px 0 var(--ink);
      text-decoration: none;
      transition: transform 150ms ease, box-shadow 150ms ease;
    }
    .upgrade-button:hover {
      text-decoration: none;
      transform: translate(-1px, -1px);
      box-shadow: 4px 4px 0 var(--ink);
    }
    '''
    html = html.replace("  </style>", new_css + "  </style>")
    print("[5/5] CSS 新增样式已插入")

    # ============================================================
    # 写入
    # ============================================================
    DST.write_text(html, encoding="utf-8")
    size_kb = DST.stat().st_size / 1024
    print(f"\n[写入] {DST}")
    print(f"  原文件: {original_len / 1024:.1f} KB")
    print(f"  公开版: {size_kb:.1f} KB")
    print(f"  增量: +{(size_kb - original_len / 1024):.1f} KB（CSS + JS 新增）")


if __name__ == "__main__":
    main()
