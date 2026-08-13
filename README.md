# AI 祛魅词典 + 编年史 · 开放查阅版

> 1327 条 AI 概念词典 + 251 个历史节点编年史，50 条精选完整样板。

## 在线访问

- 词典：`https://gengyueworks.github.io/ai-dictionary/ai-dictionary-lab.html`
- 时间轴：`https://gengyueworks.github.io/ai-dictionary/ai-timeline-design-fixed.html`

## 这是什么

一本能查、能翻、能抽卡的双语 AI 词典。

- **1327 条索引全开**：每个词条都有中英文名、类型、难度、一句释义，可搜索、可筛选、可跳转
- **50 条精选样板完整展示**：含展开理解、为何重要、记忆锚点、相关卡片等深度字段
- **闪卡复习 + 相关词跳转 + 中英切换** 全部可用
- **AI 编年史**：251 个历史节点时间轴（1936 至今），按底层突破 / 模型路线 / 产品爆发 / 生态扩散 / 安全治理 / 文化影响分类筛选，事件可跳转词典词条

## 为什么叫"开放查阅版"

完整版含 1327 条词条的深度字段（展开理解、为何重要、记忆锚点等原创加工内容），月更新增。

开放查阅版让你先看到词典的形态和含金量——50 条精选样板展示完整卡的样子，其余 1277 条只展示索引和一句释义，深度字段以模糊遮罩标记。

这不是砍掉一半的残缺品，而是让你判断"完整版值不值得入手"的样板间。

## 精选样板覆盖

| 类型 | 数量 | 代表词条 |
|------|------|---------|
| 概念 | 18 | Agent / Transformer 架构 / 图灵测试 / AI 安全 / NLP 简史 |
| 人物 | 10 | 图灵 / 辛顿 / 奥特曼 / 阿莫迪 / 卡帕西 / 黄仁勋 / 梁文锋 / 李飞飞 |
| 模型 | 8 | GPT / Claude / Gemini / Llama / Sora / Stable Diffusion / CLIP |
| 产品 | 6 | ChatGPT / Cursor / Siri / LangChain / Midjourney / AutoGPT |
| 机构 | 4 | Anthropic / Hugging Face / 苹果 / 波士顿动力 |
| 论文 | 2 | Attention Is All You Need / GPT 系列论文 |
| 系统 | 2 | AlphaFold / ELIZA |

人物类词条已补英文 aliases，搜 "Dario Amodei" 也能命中"达里奥·阿莫迪"。

## 本地运行

```bash
cd ai-dictionary
python3 -m http.server 8000
```

访问 `http://localhost:8000/ai-dictionary-lab.html`

## 移动端轻卡原型（未完成）

词典还有一个 2026-06 开发的移动端原型「AI 轻卡」：每日随机翻词卡+历史卡、小熊猫 YES 打卡、间隔回顾、学习记录页，并规划了微信小程序版。未完成、未上线，作为开发痕迹归档在 [`mobile/`](mobile/) 目录。

- 原型主文件：`mobile/ai-mobile-cards-prototype-v0.html`
- 状态与运行说明：`mobile/README.md`
- 微信小程序说明书：`mobile/AI轻卡-微信小程序项目说明书-给Agent.md`

## 目录结构

```
ai-dictionary/
├── ai-dictionary-lab.html          # 词典公开版前端（89KB）
├── ai-dictionary-free.json         # 词典公开版数据（716KB，1327 索引 + 50 精选）
├── ai-timeline-design-fixed.html   # 时间轴公开版前端（39KB）
├── ai-timeline-data-free.json      # 时间轴公开版数据（590KB，251 事件）
├── README.md
├── docs/
│   └── USAGE.md                    # 使用说明
├── mobile/                         # 移动端轻卡原型（未完成，开发痕迹归档）
│   ├── README.md                   # 状态与运行说明
│   ├── ai-mobile-cards-prototype-v0.html
│   ├── ai-learning-record.html
│   ├── AI轻卡-微信小程序项目说明书-给Agent.md
│   └── assets/                     # 小熊猫吉祥物（PNG + SVG）
└── scripts/
    ├── build-free-version.py       # 词典数据拆分脚本
    ├── build-public-html.py        # 词典前端改造脚本
    ├── build-timeline-free.py      # 时间轴数据拆分脚本
    └── build-timeline-html.py      # 时间轴前端改造脚本
```

## 数据构建

从完整版 `ai-dictionary.json` 重新生成公开版数据：

```bash
python3 scripts/build-free-version.py          # dry-run 验证精选清单
python3 scripts/build-free-version.py --write  # 实际生成 free.json
python3 scripts/build-public-html.py           # 生成公开版 HTML
```

精选清单在 `scripts/build-free-version.py` 的 `SAMPLE_TERMS` 字典里，可手动调整。

时间轴数据重建：

```bash
python3 scripts/build-timeline-free.py      # 生成 ai-timeline-data-free.json
python3 scripts/build-timeline-html.py      # 改造时间轴 HTML + 词典加回时间轴链接
```

## 技术栈

- 纯静态 HTML（单文件，无框架依赖）
- 数据：JSON（716KB，首屏加载一次）
- 部署：GitHub Pages 零成本零运维

## License

- **开放查阅版数据**（`ai-dictionary-free.json` 的索引字段）：CC BY-NC 4.0（署名-非商业性使用）
- **精选 50 条的深度字段**（definition_long / why_it_matters / memory_hook）：仅作样板展示，不得批量抓取
- **完整版内容**：不在本仓库，详见完整版协议

## 完整版

完整版含 1327 条词条的深度字段，月更新增。如需了解，请通过 Issue 联系。
