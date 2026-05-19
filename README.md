# Vibe-Coding 案例库

自动收集 GitHub 上用 vibe-coding 方式开发的项目案例。

## 技术栈

- **后端**: Python + GitHub Actions (定时收集)
- **前端**: Next.js + Tailwind CSS
- **部署**: GitHub Pages
- **AI 分析**: DeepSeek API (国产，性价比高)

## 项目结构

```
vibe-coding-cases/
├── .github/
│   └── workflows/
│       └── auto-collect.yml      # 定时收集任务
├── collector/                     # Python 收集器
│   ├── __init__.py
│   ├── github_client.py          # GitHub API 封装
│   ├── ai_analyzer.py            # AI 分析模块
│   ├── filters.py                # 过滤规则
│   └── main.py                   # 主程序
├── web/                          # Next.js 前端
│   ├── app/
│   ├── components/
│   └── data/
│       └── cases.json            # 案例数据
├── requirements.txt
└── README.md
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 填写你的 API Keys:
   - `GITHUB_TOKEN`: GitHub Personal Access Token
   - `DEEPSEEK_API_KEY`: DeepSeek API Key

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行收集器
cd collector
python main.py

# 运行前端
cd web
npm install
npm run dev
```

## 自动收集

GitHub Actions 每 6 小时自动运行收集任务，发现新的 vibe-coding 项目。

## License

MIT
