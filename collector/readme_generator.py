"""
README 自动生成器 - 支持中英文双语
从 cases.json 生成 README.md（中文）和 README_EN.md（英文）
"""
import json
import os
from datetime import datetime
from collections import defaultdict


def load_cases(data_dir: str = None):
    """加载案例数据"""
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'web', 'data')
    
    cases_file = os.path.join(data_dir, 'cases.json')
    
    if not os.path.exists(cases_file):
        return []
    
    with open(cases_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('cases', [])


def format_date(date_str: str) -> str:
    """格式化日期为简短格式"""
    if not date_str:
        return ''
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str[:10] if len(date_str) >= 10 else date_str


def generate_readme_chinese(cases: list) -> str:
    """生成中文 README"""
    by_category = defaultdict(list)
    for case in cases:
        category = case.get('category', '其他')
        by_category[category].append(case)
    
    category_emojis = {
        '网站': '🌐', '工具': '🛠️', '游戏': '🎮', '数据': '📊',
        '插件': '🔌', '应用': '📱', '创意': '🎨', '学习': '📚',
    }
    
    category_descriptions = {
        '网站': '博客、落地页、作品集、文档站等网站类项目',
        '工具': '待办清单、记账、翻译、文件处理等实用工具',
        '游戏': '小游戏、娱乐项目',
        '数据': '看板、爬虫、图表、数据分析工具',
        '插件': 'Chrome 扩展、VS Code 插件、浏览器扩展',
        '应用': '聊天App、管理后台、SaaS 等完整应用',
        '创意': '生成艺术、音乐、AI写作、实验性项目',
        '学习': '教程Demo、课程作业、技术实验',
    }
    
    category_order = ['网站', '工具', '应用', '数据', '游戏', '插件', '创意', '学习']
    
    lines = []
    
    # Header
    lines.append('<div align="center">')
    lines.append('')
    lines.append('# 🧠 Vibe-Coding 案例库')
    lines.append('')
    lines.append('发现用 AI 辅助编程开发的优秀项目')
    lines.append('')
    lines.append(f'**{len(cases)}** 个案例 · [English Version](README_EN.md) · [关于本项目](ABOUT.md)')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    
    # 关于
    lines.append('## 关于')
    lines.append('')
    lines.append('这个仓库收集了 GitHub 上用 AI 辅助编程工具（Cursor、Claude、v0、Bolt 等）开发的**真实应用案例**。')
    lines.append('')
    lines.append('- 看看别人怎么用 AI 写代码')
    lines.append('- 发现有趣的 vibe-coding 项目')
    lines.append('- 学习 AI 工具 + 技术栈的组合')
    lines.append('')
    
    # 分类目录
    lines.append('## 分类')
    lines.append('')
    lines.append('| 分类 | 说明 | 数量 |')
    lines.append('|------|------|------|')
    
    for category in category_order:
        if category in by_category:
            emoji = category_emojis.get(category, '📦')
            desc = category_descriptions.get(category, '')
            count = len(by_category[category])
            lines.append(f'| {emoji} [{category}](#{category}) | {desc} | {count} |')
    
    lines.append('')
    
    # 各分类案例
    lines.append('---')
    lines.append('')
    
    for category in category_order:
        if category not in by_category:
            continue
            
        category_cases = by_category[category]
        emoji = category_emojis.get(category, '📦')
        desc = category_descriptions.get(category, '')
        count = len(category_cases)
        
        category_cases.sort(key=lambda x: x.get('stars', 0), reverse=True)
        
        lines.append(f'<details>')
        lines.append(f'<summary><h2>{emoji} {category} <small>({count} 个项目)</small></h2></summary>')
        lines.append('')
        lines.append(f'*{desc}*')
        lines.append('')
        
        for case in category_cases:
            name = case.get('name', 'Unknown')
            description = case.get('chinese_description') or case.get('description') or ''
            stars = case.get('stars', 0)
            language = case.get('language', '')
            ai_tools = case.get('ai_tools', [])
            homepage = case.get('homepage', '')
            html_url = case.get('html_url', '')
            pushed_at = case.get('pushed_at', '')
            
            links = []
            if homepage:
                links.append(f'[演示]({homepage})')
            links.append(f'[源码]({html_url})')
            links_str = ' · '.join(links)
            
            lines.append(f'**[{name}]({html_url})** — {description}')
            lines.append('')
            
            tags = []
            if language:
                tags.append(f'`{language}`')
            if ai_tools:
                tags.append(f"🤖 {', '.join(ai_tools[:2])}")
            tags.append(f'⭐ {stars}')
            
            update_date = format_date(pushed_at)
            if update_date:
                tags.append(f'📅 {update_date}')
            
            lines.append(f'{links_str} · {" · ".join(tags)}')
            lines.append('')
        
        lines.append('---')
        lines.append('</details>')
        lines.append('')
    
    # Footer
    lines.append('---')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('')
    lines.append('**自动收集 · 每日更新**')
    lines.append('')
    lines.append(f'最后更新: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append('')
    lines.append('</div>')
    
    return '\n'.join(lines)


def generate_readme_english(cases: list) -> str:
    """生成英文 README"""
    by_category = defaultdict(list)
    for case in cases:
        category = case.get('category', 'Other')
        # 中文分类转英文
        category_map = {
            '网站': 'Websites', '工具': 'Tools', '游戏': 'Games',
            '数据': 'Data', '插件': 'Plugins', '应用': 'Apps',
            '创意': 'Creative', '学习': 'Learning'
        }
        en_category = category_map.get(category, category)
        by_category[en_category].append(case)
    
    category_emojis = {
        'Websites': '🌐', 'Tools': '🛠️', 'Games': '🎮', 'Data': '📊',
        'Plugins': '🔌', 'Apps': '📱', 'Creative': '🎨', 'Learning': '📚',
    }
    
    category_descriptions = {
        'Websites': 'Blogs, landing pages, portfolios, documentation sites',
        'Tools': 'Todo lists, accounting, translation, file processing utilities',
        'Games': 'Small games, entertainment projects',
        'Data': 'Dashboards, crawlers, charts, data analysis tools',
        'Plugins': 'Chrome extensions, VS Code plugins, browser extensions',
        'Apps': 'Chat apps, admin panels, SaaS, complete applications',
        'Creative': 'Generative art, music, AI writing, experimental projects',
        'Learning': 'Tutorial demos, course projects, tech experiments',
    }
    
    category_order = ['Websites', 'Tools', 'Apps', 'Data', 'Games', 'Plugins', 'Creative', 'Learning']
    
    lines = []
    
    # Header
    lines.append('<div align="center">')
    lines.append('')
    lines.append('# 🧠 Vibe-Coding Cases')
    lines.append('')
    lines.append('Discover awesome projects built with AI-assisted programming')
    lines.append('')
    lines.append(f'**{len(cases)}** cases · [中文版本](README.md) · [About This Project](ABOUT_EN.md)')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    
    # About
    lines.append('## About')
    lines.append('')
    lines.append('This repository collects **real application cases** from GitHub built with AI-assisted programming tools (Cursor, Claude, v0, Bolt, etc.).')
    lines.append('')
    lines.append('- See how others code with AI')
    lines.append('- Discover interesting vibe-coding projects')
    lines.append('- Learn AI tool + tech stack combinations')
    lines.append('')
    
    # Categories
    lines.append('## Categories')
    lines.append('')
    lines.append('| Category | Description | Count |')
    lines.append('|----------|-------------|-------|')
    
    for category in category_order:
        if category in by_category:
            emoji = category_emojis.get(category, '📦')
            desc = category_descriptions.get(category, '')
            count = len(by_category[category])
            anchor = category.lower().replace(' ', '-')
            lines.append(f'| {emoji} [{category}](#{anchor}) | {desc} | {count} |')
    
    lines.append('')
    
    # Cases by category
    lines.append('---')
    lines.append('')
    
    for category in category_order:
        if category not in by_category:
            continue
            
        category_cases = by_category[category]
        emoji = category_emojis.get(category, '📦')
        desc = category_descriptions.get(category, '')
        count = len(category_cases)
        anchor = category.lower().replace(' ', '-')
        
        category_cases.sort(key=lambda x: x.get('stars', 0), reverse=True)
        
        lines.append(f'<details>')
        lines.append(f'<summary><h2>{emoji} {category} <small>({count} projects)</small></h2></summary>')
        lines.append('')
        lines.append(f'*{desc}*')
        lines.append('')
        
        for case in category_cases:
            name = case.get('name', 'Unknown')
            # 优先使用英文描述，没有则用中文
            description = case.get('english_description') or case.get('chinese_description') or case.get('description') or ''
            stars = case.get('stars', 0)
            language = case.get('language', '')
            ai_tools = case.get('ai_tools', [])
            homepage = case.get('homepage', '')
            html_url = case.get('html_url', '')
            pushed_at = case.get('pushed_at', '')
            
            links = []
            if homepage:
                links.append(f'[Demo]({homepage})')
            links.append(f'[Source]({html_url})')
            links_str = ' · '.join(links)
            
            lines.append(f'**[{name}]({html_url})** — {description}')
            lines.append('')
            
            tags = []
            if language:
                tags.append(f'`{language}`')
            if ai_tools:
                tags.append(f"🤖 {', '.join(ai_tools[:2])}")
            tags.append(f'⭐ {stars}')
            
            update_date = format_date(pushed_at)
            if update_date:
                tags.append(f'📅 {update_date}')
            
            lines.append(f'{links_str} · {" · ".join(tags)}')
            lines.append('')
        
        lines.append('---')
        lines.append('</details>')
        lines.append('')
    
    # Footer
    lines.append('---')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('')
    lines.append('**Auto-collected · Daily updates**')
    lines.append('')
    lines.append(f'Last updated: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append('')
    lines.append('</div>')
    
    return '\n'.join(lines)


def generate_readme(cases: list, output_path: str = None):
    """生成中英文两个 README 文件"""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    
    # 生成中文版本
    chinese_content = generate_readme_chinese(cases)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(chinese_content)
    print(f"README.md (中文) 已生成")
    
    # 生成英文版本
    en_path = output_path.replace('README.md', 'README_EN.md')
    english_content = generate_readme_english(cases)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(english_content)
    print(f"README_EN.md (English) 已生成")
    
    # 统计
    by_category = defaultdict(list)
    for case in cases:
        by_category[case.get('category', '其他')].append(case)
    
    print(f"共 {len(cases)} 个案例, {len(by_category)} 个分类")
    
    return chinese_content, english_content


if __name__ == '__main__':
    cases = load_cases()
    generate_readme(cases)
