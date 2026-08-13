# AI 轻卡 · 移动端原型

> ⚠️ **状态：未完成原型（v0）** · Status: Unfinished Prototype (v0)
>
> 这是 AI 词典的移动端尝试，2026-06 开发，未完成、未上线。整理归档进仓库，作为项目的一部分保留开发痕迹。

This is the mobile attempt of the AI dictionary, built in June 2026. It is incomplete and never shipped. Archived here so the project keeps its development history.

---

## 这是什么 / What This Is

**AI 轻卡** —— 一个移动端优先的 AI 知识学习卡片应用，定位是「等在电梯里刷两张的轻学习卡片」。

- **每日随机翻卡**：每次展示 3 张历史事件卡 + 3 张词典词卡，可「换一段历史」「换一个词」
- **YES 点亮打卡**：卡片展开后有「YES」按钮（小熊猫掌印样式），点击标记已学，写进 localStorage
- **间隔回顾**：点过的卡片在 1/3/7/15/30 天后出现在回顾区提醒再看
- **学习记录页**：独立页面，统计每天点亮了多少卡
- **庆祝弹窗**：点亮卡片后弹出小熊猫吉祥物 + 「今天很可以」
- **相关词跳转**：词卡与历史卡互相推荐相关术语 chips

**English:** AI Light Cards is a mobile-first card app for learning AI concepts and history — flip random cards daily, mark them learned with the red panda mascot, get spaced-repetition reviews, and check your streak in the record page.

## 文件清单 / Files

| 文件 / File | 说明 / Description |
|---|---|
| `ai-mobile-cards-prototype-v0.html` | 移动端主原型（单文件 HTML/CSS/JS，约 1620 行） |
| `ai-learning-record.html` | 学习记录页（读取同一 localStorage key `ai-mobile-learned-v1`） |
| `AI轻卡-微信小程序项目说明书-给Agent.md` | 微信小程序开发 brief（下一步方向，未开工） |
| `assets/red-panda-mascot-soft-popup-512.png` | 小熊猫吉祥物（庆祝弹窗用） |
| `assets/red-panda-mascot-v1.svg` | 小熊猫 SVG 矢量版 |

## 如何运行 / How to Run

原型依赖两份**完整版数据**（不在本仓库，SSOT 在本地工作区）：

- `ai-dictionary.json` —— 词典卡片
- `ai-timeline-data.json` —— 历史时间轴

```bash
# 1. 把两份数据复制到 mobile/ 目录（数据来自本地工作区 SSOT）
cp <SSOT路径>/ai-dictionary.json mobile/
cp <SSOT路径>/ai-timeline-data.json mobile/

# 2. 本地起服务
python3 -m http.server 18765 --bind 127.0.0.1 --directory .

# 3. 手机/浏览器访问
# http://localhost:18765/mobile/ai-mobile-cards-prototype-v0.html
```

## 当前状态 / Current State

**已实现 / Implemented：** 随机翻卡、YES 点亮、学习记录、间隔回顾、庆祝弹窗、相关词跳转。

**未完成 / Missing：**

- 没有搜索、分类、难度筛选入口（只能随机翻）
- 没有「上次看到哪」的进度记忆锚点
- 微信小程序版只写了项目说明书，未开始开发
- 2026-06-08 巡检记录：移动端触控目标尺寸偏小（顶部按钮、筛选 chip 低于 44px）、`shortText()` 硬截断无尾词保护

## 数据格式 / Data Notes

- 学习记录存储在 `localStorage["ai-mobile-learned-v1"]`
- 原型用 `normalizeTerm()` 映射词典字段（`definition_short` / `front`、`why_it_matters`、`examples`、`memory_hook` / `back`、`related_terms`）
- 数据加载：`init()` 里 `Promise.all([loadJSON("ai-dictionary.json"), loadJSON("ai-timeline-data.json")])`

## 历史 / History

- 2026-06-08：移动端与网页巡检报告（含 Kimi UX 审阅建议），原型与学习记录页、小熊猫素材齐备
- 2026-06 中：写微信小程序项目说明书，规划把移动端网站做成小程序（方案 B：JSON 放云存储，启动时 fetch）
- 2026-08-13：整理归档进 `gengyueworks/ai-dictionary` 仓库的 `mobile/` 目录

## 下一步（如果要继续）/ Next Steps (If Resumed)

1. 读 `AI轻卡-微信小程序项目说明书-给Agent.md`，用小程序框架（原生 / Taro / uni-app）重写
2. 数据改走云存储或 API，卡片更新不用重新发版
3. 补搜索/筛选入口与进度记忆
4. 保持暖色纸质风 + 小熊猫吉祥物
