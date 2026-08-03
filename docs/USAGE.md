# 使用说明

## 在线访问

- 词典：`https://gengyueworks.github.io/ai-dictionary/ai-dictionary-lab.html`
- 时间轴：`https://gengyueworks.github.io/ai-dictionary/ai-timeline-design-fixed.html`

## 功能说明

### 搜索

顶部搜索框支持中英文词条名、别名匹配。人物类词条已补英文 aliases，搜 "Dario Amodei" 也能命中"达里奥·阿莫迪"。

### 筛选

- **主题**：模型训练与调优 / AI 产品与应用 / 人与机构 / AI 基础概念 等
- **类型**：concept / person / model / product / company / paper / system
- **难度**：入门 / 进阶 / 深入

### 闪卡复习

点击闪卡区域翻面，"认识"/"待复习"进度记录在 localStorage。

### 相关词跳转

词条详情页的"相关卡片""相关人物"可点击跳转。非精选词条跳转后只展示索引和一句释义，深度字段以模糊遮罩标记。

## 开放查阅版 vs 完整版

| 字段 | 开放查阅版 | 完整版 |
|------|-----------|--------|
| 索引（term / term_zh / type / difficulty） | 1327 条全开 | 1327 条 |
| 一句释义（definition_short） | 1327 条全开 | 1327 条 |
| 展开理解（definition_long） | 仅 50 条精选 | 全部 |
| 为何重要（why_it_matters） | 仅 50 条精选 | 全部 |
| 记忆锚点（memory_hook） | 仅 50 条精选 | 全部 |
| 相关词跳转 | 可用 | 可用 |
| 闪卡复习 | 可用 | 可用 |
| 更新频率 | 半年一次 | 月更 |

## 本地部署

```bash
git clone https://github.com/gengyueworks/ai-dictionary.git
cd ai-dictionary
python3 -m http.server 8000
```

访问 `http://localhost:8000/ai-dictionary-lab.html`

## 重新构建数据

如果你是维护者，从完整版 `ai-dictionary.json` 重新生成公开版：

```bash
# 1. 把完整版 ai-dictionary.json 放到源头目录
# 2. 修改 scripts/build-free-version.py 里的 SRC 路径
# 3. 运行
python3 scripts/build-free-version.py --write
python3 scripts/build-public-html.py
```

精选清单调整：编辑 `scripts/build-free-version.py` 的 `SAMPLE_TERMS` 字典。

## 浏览器兼容

- Chrome / Edge / Safari 最近 2 个版本
- 不支持 IE


## AI 编年史（时间轴）

### 功能

- **251 个历史节点**：从 1936 年 Turing Bombe 到 2026 年最新事件
- **分类筛选**：底层突破 / 模型路线 / 产品爆发 / 生态扩散 / 安全治理 / 文化影响
- **搜索**：按年份、事件、概念搜索
- **事件跳转词典**：每个事件的相关词可跳转到词典词条

### 时间轴分层

| 字段 | 开放查阅版 | 完整版 |
|------|-----------|--------|
| 事件基本信息（年份 / 标题 / 摘要 / 类型） | 251 条全开 | 251 条 |
| 相关词跳转 | 可用 | 可用 |
| 背后现场（behind_scenes_zh） | 模糊遮罩 | 全部 |
| 为何重要（why_it_matters_zh） | 模糊遮罩 | 全部 |
| 学习路径（learning_path_hint） | 不展示 | 全部 |

### 词典与时间轴互通

- 词典顶部"← 时间轴"按钮 → 跳转时间轴
- 时间轴顶部"词典 →"按钮 → 跳转词典
- 时间轴事件的相关词点击 → 跳转词典对应词条
