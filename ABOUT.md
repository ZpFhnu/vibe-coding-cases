<div align="center">

# 关于本项目

**Vibe-Coding 案例库 —— 全自动 AI 项目收集系统**

[English Version](ABOUT_EN.md)

</div>

---

## 📖 项目简介

这是一个**完全自动化**的 GitHub 项目收集系统，专门收集使用 AI 辅助编程（Vibe-Coding）方式开发的优秀项目。

**核心特点**：
- 🤖 **零人工干预** —— 从发现项目到生成展示页面，全程自动化
- 🔄 **每日自动更新** —— 每天自动搜索、分析、收录新项目
- 🌍 **双语支持** —— 同时生成中文和英文版本
- 📊 **智能分类** —— AI 自动判断项目类型（网站/工具/应用等）

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    自动收集流程                          │
├─────────────────────────────────────────────────────────┤
│  1. GitHub Actions 定时触发（每天 0:00）                  │
│                      ↓                                  │
│  2. Python 脚本搜索 GitHub 项目                          │
│     • 19 个关键词组合搜索                                │
│     • 智能翻页，每个关键词至少找 5 个新项目               │
│                      ↓                                  │
│  3. AI 分析（DeepSeek/智谱/通义千问）                     │
│     • 判断是否为 Vibe-Coding 项目                        │
│     • 自动提取：技术栈、AI工具、分类                     │
│     • 生成双语描述（中文+英文）                          │
│                      ↓                                  │
│  4. 质量筛选                                            │
│     • 排除教程、模板、Awesome 列表                       │
│     • 只保留实际应用案例                                 │
│                      ↓                                  │
│  5. 自动生成 README                                     │
│     • README.md（中文）                                  │
│     • README_EN.md（英文）                               │
│                      ↓                                  │
│  6. 自动提交到 GitHub                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **定时任务** | GitHub Actions | 每天自动运行 |
| **数据收集** | Python + GitHub API | 搜索和获取项目信息 |
| **AI 分析** | DeepSeek API | 国产大模型，性价比高 |
| **数据存储** | JSON 文件 | 无需数据库，简单直接 |
| **展示页面** | Markdown | GitHub 原生支持，无需部署 |

---

## 💰 成本分析

| 项目 | 费用 | 说明 |
|------|------|------|
| GitHub Actions | ¥0 | 免费额度足够 |
| GitHub API | ¥0 | 免费额度足够 |
| DeepSeek API | ~¥100/月 | 每天分析 50 个项目 |
| **总计** | **~¥100/月** | 全自动运行 |

---

## 🚀 快速开始（如果你想搭建类似项目）

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮，复制到自己的 GitHub 账号。

### 2. 配置 Secrets

进入仓库 Settings → Secrets → Actions，添加：

| Secret Name | 值 | 获取方式 |
|-------------|-----|---------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | https://github.com/settings/tokens |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | https://platform.deepseek.com |
| `AI_PROVIDER` | `deepseek` | 固定值 |

### 3. 启用 GitHub Pages

Settings → Pages → Source 选择 "GitHub Actions"

### 4. 运行收集器

进入 Actions → "Auto Collect Vibe-Coding Projects" → Run workflow

### 5. 自定义配置

修改 `.github/workflows/auto-collect.yml`：

```yaml
# 定时设置（每天 0 点）
cron: '0 0 * * *'

# 每次处理项目数
MAX_PROJECTS_PER_RUN: 50

# 最小 stars 数
MIN_STARS: 5
```

---

## 📁 项目结构

```
vibe-coding-cases/
├── .github/workflows/          # GitHub Actions 配置
│   ├── auto-collect.yml        # 自动收集主流程
│   ├── add-english.yml         # 添加英文描述（手动）
│   └── reclassify.yml          # 重新分类（手动）
├── collector/                  # Python 收集器
│   ├── github_client.py        # GitHub API 封装
│   ├── ai_analyzer.py          # AI 分析模块
│   ├── data_store.py           # 数据存储
│   ├── readme_generator.py     # README 生成器
│   ├── main.py                 # 主程序
│   ├── add_english.py          # 添加英文描述
│   └── reclassify.py           # 重新分类
├── web/data/                   # 数据文件
│   └── cases.json              # 案例数据
├── README.md                   # 中文展示页（自动生成）
├── README_EN.md                # 英文展示页（自动生成）
├── ABOUT.md                    # 本文件
└── ABOUT_EN.md                 # 英文版介绍
```

---

## 🔧 自定义开发

### 修改搜索关键词

编辑 `collector/github_client.py`：

```python
search_queries = [
    '"vibe coding" in:readme',
    '"built with cursor" in:readme',
    # 添加你的关键词...
]
```

### 修改分类标准

编辑 `collector/ai_analyzer.py`：

```python
VALID_CATEGORIES = ['网站', '工具', '游戏', '数据', '插件', '应用', '创意', '学习']
```

### 更换 AI 提供商

支持 DeepSeek、智谱、通义千问、Kimi：

```python
# 在 GitHub Secrets 中设置
AI_PROVIDER=deepseek  # 或 zhipu / qwen / kimi
```

---

## ⚠️ 注意事项

1. **GitHub API 限制**：每小时最多 5000 次请求
2. **AI API 费用**：按使用量计费，注意控制成本
3. **数据隐私**：收集的都是公开仓库，不涉及隐私问题

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

如果你想：
- 添加新功能
- 修复 Bug
- 改进文档
- 分享你的使用案例

请随时联系我们。

---

## 📄 许可证

MIT License — 可自由使用、修改、分发。

---

<div align="center">

**Made with ❤️ and AI**

</div>
