# SSOT 重定向说明

> 本文件是 SSOT 声明，不是站点文档。请勿删除。

**本仓库（ai-dictionary 公开仓库）不是主源。**

## 主源

AI 词典的唯一主源（SSOT）：

```
/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/ai-dictionary.json
```

规模：1327 条。

> **EN —** This public repo (ai-dictionary) is **not** the master source. The single SSOT for the AI dictionary is the **absolute path above** (`ai-dictionary.json`, 1,327 entries). All data changes must be made there, never here.

## 本仓库内文件的身份

- `ai-dictionary-free.json`：**构建产物**，由主源构建生成，用于公开站点展示。
- `ai-dictionary-free-en.json`：**构建产物**，主源的英文翻译发布版。
- `ai-timeline-data-free.json`、`ai-timeline-design-fixed.html`：时间轴的发布产物（时间轴主源见 ai-timeline 的 SSOT 重定向说明）。

> **EN —** The JSON files in this repo are **build artifacts**, generated from the master source for public site display — they are not the data source. `ai-dictionary-free.json` is the public build of the dictionary; `ai-dictionary-free-en.json` is its English release; the timeline files are release artifacts (see the ai-timeline SSOT redirect for the timeline master source).

## 写入方向

```
主源（ai-dictionary.json） → 构建流程 → 本仓库发布 JSON
```

- 数据变更一律写主源，然后由构建流程重新生成发布 JSON。
- **禁止直接编辑本仓库的发布 JSON 作为数据源**，直接改动会在下次构建时被覆盖。

> **EN —** Write direction: master source (`ai-dictionary.json`) → build pipeline → published JSON in this repo. Change data only in the master source, then let the build regenerate the published JSON. **Directly editing the published JSON in this repo as a data source is forbidden** — manual edits will be overwritten on the next build.

## 相关规则

完整的主源清单、写入方向和禁止事项见：

```
/Volumes/拓展坞 1T2022/2 Codex-Workspace/Codex-Workspace-Main/32-AI高质量阅读库/05-情报与深读系统/AI精华情报与深读操作台/10-源头网站活文件/00-站点根文件/_flow/ssot-manifest.md
```
