# 🚀 部署指南

## 项目结构

```
vibe-coding-cases/
├── .github/workflows/
│   ├── auto-collect.yml    # 自动收集任务
│   └── deploy.yml          # 自动部署到 GitHub Pages
├── collector/              # Python 收集器
│   ├── github_client.py
│   ├── ai_analyzer.py
│   ├── data_store.py
│   └── main.py
├── web/                    # Next.js 前端
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── data/              # 数据文件
└── README.md
```

## 部署步骤

### 1. 创建 GitHub 仓库

1. 在 GitHub 上创建一个新仓库，命名为 `vibe-coding-cases`
2. 将代码推送到仓库

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/vibe-coding-cases.git
git push -u origin main
```

### 2. 配置 Secrets

在 GitHub 仓库页面 → Settings → Secrets and variables → Actions 中添加以下 secrets：

| Secret Name | 说明 | 获取方式 |
|------------|------|---------|
| `GITHUB_TOKEN` | GitHub API Token | https://github.com/settings/tokens |
| `DEEPSEEK_API_KEY` | DeepSeek API Key (推荐) | https://platform.deepseek.com |
| `AI_PROVIDER` | AI 提供商 | 填 `deepseek` |

可选（如果使用其他 AI）：
- `ZHIPU_API_KEY` - 智谱 AI
- `DASHSCOPE_API_KEY` - 通义千问
- `MOONSHOT_API_KEY` - Kimi

#### 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 和 `read:org` 权限
4. 生成后复制 token

#### 获取 DeepSeek API Key

1. 访问 https://platform.deepseek.com
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key

### 3. 启用 GitHub Pages

1. 进入仓库 Settings → Pages
2. Source 选择 "GitHub Actions"
3. 保存

### 4. 运行收集器

#### 方式一：手动触发

1. 进入仓库 Actions 页面
2. 选择 "Auto Collect Vibe-Coding Projects"
3. 点击 "Run workflow"

#### 方式二：等待自动运行

收集器会每 6 小时自动运行一次。

### 5. 查看网站

部署完成后，网站将发布在：

```
https://yourusername.github.io/vibe-coding-cases
```

## 本地测试

### 测试收集器

```bash
# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env
# 编辑 .env 填入你的 API keys

# 运行收集器
cd collector
python main.py
```

### 测试前端

```bash
cd web

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build
```

## 配置说明

### 收集器配置

在 GitHub Secrets 中配置：

| 配置项 | 默认值 | 说明 |
|-------|-------|------|
| `MIN_STARS` | 5 | 最小 stars 数 |
| `MAX_PROJECTS_PER_RUN` | 30 | 每次运行最多处理项目数 |
| `MIN_CONFIDENCE` | 0.75 | AI 置信度阈值 |
| `MIN_QUALITY` | 6 | 质量分阈值 |

### 成本估算

使用 DeepSeek API：
- 每次分析约 ¥0.01-0.03
- 每天运行 4 次，每次分析 30 个项目
- 月成本约 ¥30-90

## 故障排除

### 收集器运行失败

1. 检查 Secrets 是否正确配置
2. 查看 Actions 日志获取详细错误信息
3. 确认 API Key 有足够余额

### 网站没有更新

1. 检查 deploy workflow 是否成功
2. 确认 GitHub Pages 设置正确
3. 清除浏览器缓存

### AI 分析失败

1. 检查 API Key 是否有效
2. 确认 API Key 有足够额度
3. 尝试切换其他 AI 提供商

## 自定义

### 修改搜索关键词

编辑 `collector/github_client.py` 中的 `search_vibe_coding_projects` 方法。

### 修改前端样式

编辑 `web/app/components/` 中的组件。

### 添加新功能

1. 后端：在 `collector/` 中添加新模块
2. 前端：在 `web/app/` 中添加新页面或组件

## 更新

要更新到最新版本：

```bash
git pull origin main
```

然后重新部署。

## 支持

如有问题，请提交 Issue 或联系维护者。
