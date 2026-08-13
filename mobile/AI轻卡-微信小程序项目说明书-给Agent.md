# AI 轻卡 · 微信小程序项目说明书

> 给腾讯 CodeBuddy / 任何 Agent 的项目启动 brief。
> 目标：把已有的 AI 词典移动端网站，做成一个微信小程序。

---

## 一、项目是什么

**AI 轻卡** —— 一个移动端优先的 AI 知识学习卡片应用。核心功能：

1. **词卡**（Dictionary Cards）：每张卡是一个 AI 概念（Transformer、RAG、Agent……），卡片可展开，展示一句话解释、为何重要、记忆技巧、举例、关联术语
2. **时间轴**（Timeline Cards）：AI 历史事件卡片，每张记录 AI 领域的一个里程碑事件
3. **间隔回顾**（Spaced Repetition）：点过的卡片会在 1/3/7/15/30 天后提醒回顾
4. **学习记录**：localStorage 记录每天点亮了多少卡
5. **庆祝弹窗**：每次点卡后弹出「今天很可以」的鼓励弹窗，带小熊猫吉祥物

**定位**：不是严肃的词典工具，是「等在电梯里刷两张的轻学习卡片」。

---

## 二、现状：已有移动端网站

### 2.1 入口文件

```
/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/
  ├── ai-mobile-cards-prototype-v0.html   <-- 移动端主文件（1620行，单文件HTML/CSS/JS）
  ├── ai-dictionary.json                  <-- 词典数据 SSOT（~1100 张卡片）
  ├── ai-timeline-data.json               <-- 时间轴数据 SSOT（~189 件事）
  └── assets/
      ├── red-panda-mascot-soft-popup-512.png   <-- 小熊猫吉祥物图（弹窗用）
      └── red-panda-mascot-v1.svg                <-- 小熊猫 SVG

### 2.2 数据加载方式

移动端在 `init()` 函数中 fetch 两个 JSON 文件：

```js
const [dictionary, timeline] = await Promise.all([
  loadJSON("ai-dictionary.json"),
  loadJSON("ai-timeline-data.json")
]);
```

**这意味着：小程序只需要把 JSON 放进去或通过 API 获取，不需要改数据结构。**

### 2.3 服务方式

用 Python HTTP Server 在本地 `127.0.0.1:18765` 提供服务：
```bash
python3 -m http.server 18765 --bind 127.0.0.1 --directory <站点根目录>
```

---

## 三、数据结构

### 3.1 词典卡片（ai-dictionary.json）

```json
{
  "generated_at": "2026-06-02T13:51:10",
  "terms": [
    {
      "id": "transformer",
      "term": "Transformer",
      "term_zh": "Transformer",
      "aliases": ["Transformer"],
      "entry_type": "concept",
      "category": "概念底座",
      "difficulty": "进阶",
      "definition_short": "一句话定义，放在卡片背面",
      "back": "卡片背面内容（记忆钩子）",
      "front": "卡片正面问题（如：Transformer是什么？）",
      "definition_long": "详细解释，500-800字",
      "examples": ["例子1", "例子2"],
      "source_links": ["https://en.wikipedia.org/wiki/...", "..."],
      "related_people": ["Geoffrey Hinton", "..."],
      "why_it_matters": "这段知识为什么重要",
      "memory_hook": "记忆钩子——怎么记住这个概念",
      "related_terms": ["注意力机制", "BERT", "GPT"],
      "updated_at": "2026-06-18",
      "source_note": "v2:新写。model_used:deepseek-v4-flash"
    }
  ]
}
```

### 3.2 时间轴事件（ai-timeline-data.json）

```json
{
  "timeline": [
    {
      "title_zh": "ChatGPT 发布",
      "title_en": "ChatGPT Released",
      "date": "2022-11-30",
      "year": 2022,
      "summary_zh": "事件概述",
      "why_it_matters_zh": "这件事为什么重要",
      "behind_scenes_zh": "背后现场/内幕",
      "related_terms": ["GPT-3.5", "OpenAI", "RLHF"],
      "related_card_ids": ["gpt-3.5", "openai", "rlhf"]
    }
  ]
}
```

### 3.3 移动端如何映射字段

移动端的 `normalizeTerm()` 函数（ai-mobile-cards-prototype-v0.html 第1292行）：

```js
function normalizeTerm(term) {
  return {
    term: term.term || "",
    termZh: term.term_zh || "",
    category: term.category || "AI 词条",
    id: `term-${slug(term.id || term.term || term.term_zh)}`,
    short: term.definition_short || term.front || "",       // ← 卡片正面一句话
    why: term.why_it_matters || "",                          // ← 为何重要
    example: term.examples?.[0] || "",                       // ← 例子
    hook: term.memory_hook || term.back || "",               // ← 记忆钩子
    related: term.related_terms?.slice(0, 4) || []           // ← 关联术语（最多4个）
  };
}
```

---

## 四、移动端 UI 设计参考

### 4.1 整体风格

- **配色**：纸质暖色调（`#f6f3ed` 纸白背景、`#1d1a16` 墨色文字）
- **字体**：系统默认（`-apple-system, PingFang SC, Microsoft YaHei`）
- **容器**：`max-width: 440px`，居中显示，移动优先
- **卡片**：圆角 19px，柔阴影，点击展开 `<details>` 元素

### 4.2 页面结构（从上到下）

1. **操作栏**（sticky 顶部）：两个按钮——「换一段历史」「换一个词」
2. **回顾区**（可选显示）：到期该回看的卡片，基于 localStorage 的间隔记忆算法
3. **时间轴区**：每次展示 3 张历史事件卡片
4. **词卡区**：每次展示 3 张词典卡片
5. **右下角浮动按钮**：跳转学习记录页
6. **Toast 通知**（底部居中）：显示学习进度
7. **庆祝弹窗**（全屏蒙层）：点亮卡片后弹出，小熊猫图片 + 「今天很可以」

### 4.3 卡片交互

- 卡片是 `<details>` 折叠元素，点击展开露出详细信息
- 展开后底部有「YES」按钮（小熊猫掌印样式），点击标记已学
- 每个卡片有关联术语 chip，点击跳转到对应卡片

### 4.4 小熊猫吉祥物

小熊猫（Red Panda）是整个产品的 mascot。图标已经在 assets 目录里：
- `red-panda-mascot-soft-popup-512.png` —— 弹窗用的 512px 软萌小熊猫
- `red-panda-mascot-v1.svg` —— SVG 矢量版

小程序需要复用这个吉祥物形象。

---

## 五、目标：做微信小程序

### 5.1 具体要求

1. **用微信小程序框架**（原生或 Taro/uni-app 均可，你选你最熟的）
2. **数据来源**：把 `ai-dictionary.json` 和 `ai-timeline-data.json` 放到小程序项目里，或者通过一个简单的云函数/API 提供（JSON 文件会持续更新，新的卡片会不断加进去）
3. **核心交互**：
   - 词卡和时间轴卡片的展示、展开、切换
   - 「YES」点亮卡片的学习记录（用微信小程序的本地存储替代 localStorage）
   - 间隔回顾提醒
   - 庆祝弹窗（带小熊猫图片）
4. **页面至少要有**：
   - 主页（卡片浏览）
   - 学习记录页（展示学习统计）
5. **设计保持移动端网站的风格**：暖色纸质感、圆角卡片、小熊猫吉祥物

### 5.2 不是从零开始

- **不需要重新设计**——直接参考 `ai-mobile-cards-prototype-v0.html` 的设计语言
- **不需要重新写数据**——JSON 文件是现成的，字段已经定义好了
- **不需要重新画吉祥物**——小熊猫图片已经有了

### 5.3 数据更新策略

JSON 文件会持续更新（目前约 1100 张卡，每周还在增加）。小程序需要考虑：
- 方案 A：JSON 文件直接打包进小程序，更新时重新提交审核
- 方案 B：JSON 放云开发/云存储，小程序启动时 fetch 最新数据（推荐）
- 方案 C：用云函数提供 API，从数据库读取

**推荐方案 B**，最灵活，卡片增加不需要重新发版。

---

## 六、文件位置汇总（绝对路径）

| 文件 | 路径 |
|------|------|
| 移动端主文件 | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-mobile-cards-prototype-v0.html` |
| 词典数据 SSOT | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-dictionary.json` |
| 时间轴数据 SSOT | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-timeline-data.json` |
| 小熊猫 PNG | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/assets/red-panda-mascot-soft-popup-512.png` |
| 小熊猫 SVG | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/assets/red-panda-mascot-v1.svg` |
| 启动脚本 | `/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/serve_ai_learning_site.sh` |

---

## 七、给 Agent 的行动建议

1. **先读** `ai-mobile-cards-prototype-v0.html` 里 1200-1620 行的 JS 逻辑，搞懂数据怎么加载和卡片怎么渲染
2. **选一个小程序框架**（Taro/uni-app 或者微信原生），创建一个新项目
3. **把 JSON 数据文件复制到小程序项目中**
4. **按照移动端的 UI，用小程序组件重写一遍**（不需要一模一样，但保持暖色纸质感和卡片交互）
5. **实现 localStorage → wx.setStorageSync 的迁移**
6. **加一个学习记录页**
7. **测试，然后告诉我需要什么权限/配置才能上传到微信小程序后台**

如果遇到任何问题——数据结构不清楚、某个交互不知道怎么实现——直接在这个说明书的文件旁边创建一个备注文件记录下来，我们一起看。
