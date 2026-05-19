<div align="center">

# About This Project

**Vibe-Coding Cases — Fully Automated AI Project Collection System**

[中文版本](ABOUT.md)

</div>

---

## 📖 Project Overview

This is a **fully automated** GitHub project collection system that discovers and showcases outstanding projects built with AI-assisted programming (Vibe-Coding).

**Key Features**:
- 🤖 **Zero Manual Intervention** — From discovery to presentation, fully automated
- 🔄 **Daily Auto-Updates** — Automatically searches, analyzes, and adds new projects daily
- 🌍 **Bilingual Support** — Generates both Chinese and English versions simultaneously
- 📊 **Smart Categorization** — AI automatically classifies projects (Websites/Tools/Apps/etc.)

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Auto-Collection Flow                   │
├─────────────────────────────────────────────────────────┤
│  1. GitHub Actions Scheduled Trigger (Daily at 0:00)    │
│                      ↓                                  │
│  2. Python Script Searches GitHub Projects              │
│     • 19 keyword combinations                           │
│     • Smart pagination, 5+ new projects per keyword     │
│                      ↓                                  │
│  3. AI Analysis (DeepSeek/Zhipu/Qwen)                   │
│     • Identifies Vibe-Coding projects                   │
│     • Auto-extracts: Tech stack, AI tools, Category     │
│     • Generates bilingual descriptions (CN+EN)          │
│                      ↓                                  │
│  4. Quality Filtering                                   │
│     • Excludes tutorials, templates, Awesome lists      │
│     • Keeps only real application cases                 │
│                      ↓                                  │
│  5. Auto-Generate README                                │
│     • README.md (Chinese)                               │
│     • README_EN.md (English)                            │
│                      ↓                                  │
│  6. Auto-Commit to GitHub                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| **Scheduling** | GitHub Actions | Runs automatically every day |
| **Data Collection** | Python + GitHub API | Searches and fetches project info |
| **AI Analysis** | DeepSeek API | Cost-effective Chinese LLM |
| **Data Storage** | JSON Files | No database needed, simple and direct |
| **Presentation** | Markdown | Native GitHub support, no deployment |

---

## 💰 Cost Analysis

| Item | Cost | Notes |
|------|------|-------|
| GitHub Actions | $0 | Free tier sufficient |
| GitHub API | $0 | Free tier sufficient |
| DeepSeek API | ~$15/month | Analyzing 50 projects daily |
| **Total** | **~$15/month** | Fully automated operation |

---

## 🚀 Quick Start (Build Your Own)

### 1. Fork This Repository

Click the "Fork" button in the top right to copy to your GitHub account.

### 2. Configure Secrets

Go to Settings → Secrets → Actions, add:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | https://github.com/settings/tokens |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | https://platform.deepseek.com |
| `AI_PROVIDER` | `deepseek` | Fixed value |

### 3. Enable GitHub Pages

Settings → Pages → Source select "GitHub Actions"

### 4. Run the Collector

Go to Actions → "Auto Collect Vibe-Coding Projects" → Run workflow

### 5. Customize Configuration

Edit `.github/workflows/auto-collect.yml`:

```yaml
# Schedule (daily at 0:00)
cron: '0 0 * * *'

# Projects per run
MAX_PROJECTS_PER_RUN: 50

# Minimum stars
MIN_STARS: 5
```

---

## 📁 Project Structure

```
vibe-coding-cases/
├── .github/workflows/          # GitHub Actions configs
│   ├── auto-collect.yml        # Main auto-collection flow
│   ├── add-english.yml         # Add English (manual)
│   └── reclassify.yml          # Reclassify (manual)
├── collector/                  # Python collector
│   ├── github_client.py        # GitHub API wrapper
│   ├── ai_analyzer.py          # AI analysis module
│   ├── data_store.py           # Data storage
│   ├── readme_generator.py     # README generator
│   ├── main.py                 # Main program
│   ├── add_english.py          # Add English descriptions
│   └── reclassify.py           # Reclassify cases
├── web/data/                   # Data files
│   └── cases.json              # Case data
├── README.md                   # Chinese showcase (auto-generated)
├── README_EN.md                # English showcase (auto-generated)
├── ABOUT.md                    # This file (Chinese)
└── ABOUT_EN.md                 # This file
```

---

## 🔧 Customization

### Modify Search Keywords

Edit `collector/github_client.py`:

```python
search_queries = [
    '"vibe coding" in:readme',
    '"built with cursor" in:readme',
    # Add your keywords...
]
```

### Modify Category Standards

Edit `collector/ai_analyzer.py`:

```python
VALID_CATEGORIES = ['Websites', 'Tools', 'Games', 'Data', 'Plugins', 'Apps', 'Creative', 'Learning']
```

### Change AI Provider

Supports DeepSeek, Zhipu, Qwen, Kimi:

```python
# Set in GitHub Secrets
AI_PROVIDER=deepseek  # or zhipu / qwen / kimi
```

---

## ⚠️ Notes

1. **GitHub API Limit**: 5000 requests per hour
2. **AI API Costs**: Pay-per-use, monitor your spending
3. **Data Privacy**: Only collects public repositories

---

## 🤝 Contributing

Issues and PRs welcome!

If you want to:
- Add new features
- Fix bugs
- Improve documentation
- Share your use case

Please reach out.

---

## 📄 License

MIT License — Free to use, modify, and distribute.

---

<div align="center">

**Made with ❤️ and AI**

</div>
