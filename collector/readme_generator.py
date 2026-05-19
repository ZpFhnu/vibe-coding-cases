"""
README 自动生成器
从 cases.json 生成漂亮的 README.md，类似 awesome-llm-apps 的风格
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


def generate_readme(cases: list, output_path: str = None):
    """生成 README.md"""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    
    # 按分类分组
    by_category = defaultdict(list)
    for case in cases:
        category = case.get('category', '其他')
        by_category[category].append(case)
    
    # 分类 emoji 映射
    category_emojis = {
        'Web应用': '🌐',
        '移动端': '📱',
        '游戏': '🎮',
        '工具': '🛠️',
        'Chrome插件': '🔌',
        'VSCode插件': '📝',
        'CLI工具': '⌨️',
        '其他': '📦',
    }
    
    # 统计 AI 工具
    ai_tools_count = defaultdict(int)
    for case in cases:
        for tool in case.get('ai_tools', []):
            ai_tools_count[tool] += 1
    
    # 排序 AI 工具
    top_ai_tools = sorted(ai_tools_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 生成 README 内容
    lines = []
    
    # ===== Header =====
    lines.append('<div align="center">')
    lines.append('')
    lines.append('# 🧠 Vibe-Coding 案例库')
    lines.append('')
    lines.append('### 发现用 AI 辅助编程开发的优秀项目，看看别人怎么用 AI 写代码')
    lines.append('')
    lines.append(f'**{len(cases)}** 个案例 · **{len(by_category)}** 个分类 · **{len(ai_tools_count)}** 种 AI 工具')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    
    # ===== 为什么有这个项目 =====
    lines.append('## 💡 为什么有这个项目')
    lines.append('')
    lines.append('Vibe-Coding（氛围编程）正在改变软件开发的方式。这个仓库收集了 GitHub 上用 AI 辅助编程工具（如 Cursor、Claude、v0、Bolt.new、Lovable 等）开发的真实项目案例。')
    lines.append('')
    lines.append('- 🎯 **对初学者**：看看别人怎么用 AI 写代码，学习 Prompt 技巧')
    lines.append('- 💡 **找灵感**：发现有趣的 vibe-coding 项目，激发你的创意')
    lines.append('- 📚 **学技术栈**：了解不同 AI 工具 + 技术栈的组合方式')
    lines.append('- ⚡ **看效率**：感受 vibe-coding 的真实开发速度')
    lines.append('')
    
    # ===== 热门 AI 工具 =====
    if top_ai_tools:
        lines.append('## 🤖 热门 AI 工具')
        lines.append('')
        tool_table = '| 工具 | 案例数 |'
        tool_table += '\n|------|--------|'
        for tool, count in top_ai_tools:
            tool_table += f'\n| {tool} | {count} |'
        lines.append(tool_table)
        lines.append('')
    
    # ===== 目录 =====
    lines.append('## 📑 分类目录')
    lines.append('')
    for category in by_category.keys():
        emoji = category_emojis.get(category, '📦')
        count = len(by_category[category])
        lines.append(f'- [{emoji} {category}](#{category.lower().replace(" ", "-")}) ({count} 个项目)')
    lines.append('')
    
    # ===== 各分类案例 =====
    lines.append('---')
    lines.append('')
    
    for category, category_cases in by_category.items():
        emoji = category_emojis.get(category, '📦')
        
        # 分类标题
        lines.append(f'## {emoji} {category}')
        lines.append('')
        
        # 按 stars 排序
        category_cases.sort(key=lambda x: x.get('stars', 0), reverse=True)
        
        for case in category_cases:
            name = case.get('name', 'Unknown')
            full_name = case.get('full_name', '')
            description = case.get('chinese_description') or case.get('description') or ''
            stars = case.get('stars', 0)
            language = case.get('language', '')
            ai_tools = case.get('ai_tools', [])
            tech_stack = case.get('tech_stack', [])
            estimated_hours = case.get('estimated_hours', '')
            homepage = case.get('homepage', '')
            html_url = case.get('html_url', '')
            
            # 项目名称行
            links = []
            if homepage:
                links.append(f'[🌐 在线体验]({homepage})')
            links.append(f'[💻 源码]({html_url})')
            links_str = ' · '.join(links)
            
            lines.append(f'### [{name}]({html_url})')
            lines.append('')
            lines.append(f'{description}')
            lines.append('')
            
            # 标签行
            tags = []
            if language:
                tags.append(f'`{language}`')
            for tool in ai_tools[:3]:
                tags.append(f'🤖 {tool}')
            for tech in tech_stack[:3]:
                tags.append(tech)
            if estimated_hours:
                tags.append(f'⏱️ {estimated_hours}')
            tags.append(f'⭐ {stars}')
            
            lines.append(f'{links_str}  ')
            lines.append(f'{", ".join(tags)}')
            lines.append('')
    
    # ===== Footer =====
    lines.append('---')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('')
    lines.append('## 📤 提交你的案例')
    lines.append('')
    lines.append('如果你用 vibe-coding 方式开发了有趣的项目，欢迎提交！')
    lines.append('')
    lines.append('本项目通过 GitHub Actions 自动收集和更新案例。')
    lines.append('')
    lines.append(f'最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")} · 数据来源: GitHub')
    lines.append('')
    lines.append('</div>')
    
    # 写入文件
    readme_content = '\n'.join(lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"README.md 已生成: {output_path}")
    print(f"共 {len(cases)} 个案例, {len(by_category)} 个分类")
    
    return readme_content


if __name__ == '__main__':
    cases = load_cases()
    generate_readme(cases)
