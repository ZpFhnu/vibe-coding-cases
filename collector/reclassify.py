"""
一次性重新分类脚本
对已有的 cases.json 重新进行 AI 分类，修复分类错误
"""
import json
import os
from datetime import datetime
from ai_analyzer import AIFactory
from data_store import DataStore


def reclassify_cases():
    """重新分类已有案例"""
    print("=" * 60)
    print("开始重新分类已有案例")
    print("=" * 60)
    
    store = DataStore()
    cases = store.load_cases()
    
    if not cases:
        print("没有案例需要重新分类")
        return
    
    print(f"共 {len(cases)} 个案例需要重新分类")
    
    # 创建 AI 分析器
    try:
        analyzer = AIFactory.create_analyzer()
    except Exception as e:
        print(f"创建 AI 分析器失败: {e}")
        return
    
    # 统计变化
    changes = []
    
    for idx, case in enumerate(cases, 1):
        print(f"\n[{idx}/{len(cases)}] 处理: {case.get('full_name', 'Unknown')}")
        print(f"  原分类: {case.get('category', '无')}")
        
        # 准备重新分析的数据
        repo_data = {
            'id': case.get('github_id'),
            'full_name': case.get('full_name'),
            'description': case.get('description', ''),
            'language': case.get('language'),
            'stargazers_count': case.get('stars', 0),
            'forks_count': case.get('forks', 0),
            'html_url': case.get('html_url'),
            'homepage': case.get('homepage'),
            'created_at': case.get('created_at'),
            'pushed_at': case.get('pushed_at'),
            'readme': case.get('readme_preview', ''),
            'file_structure': [],
            'recent_commits': []
        }
        
        try:
            # AI 重新分析
            analysis = analyzer.analyze_project(repo_data)
            
            old_category = case.get('category', '')
            new_category = analysis['category']
            
            print(f"  新分类: {new_category}")
            
            # 如果分类变了，记录变化
            if old_category != new_category:
                changes.append({
                    'name': case.get('name'),
                    'old': old_category,
                    'new': new_category,
                    'reason': analysis.get('why_vibe_coding', '')
                })
                print(f"  ✅ 分类变更: {old_category} → {new_category}")
            
            # 更新案例数据
            case['category'] = new_category
            case['chinese_description'] = analysis.get('chinese_description', case.get('chinese_description'))
            case['ai_tools'] = analysis.get('ai_tools', case.get('ai_tools', []))
            case['tech_stack'] = analysis.get('tech_stack', case.get('tech_stack', []))
            case['quality_score'] = analysis.get('quality_score', case.get('quality_score', 5))
            case['confidence'] = analysis.get('confidence', case.get('confidence', 0))
            case['why_vibe_coding'] = analysis.get('why_vibe_coding', case.get('why_vibe_coding', ''))
            case['updated_at'] = datetime.now().isoformat()
            
        except Exception as e:
            print(f"  ❌ 分析失败: {e}")
            continue
    
    # 保存更新后的数据
    store.save_cases(cases)
    
    # 打印总结
    print("\n" + "=" * 60)
    print("重新分类完成!")
    print("=" * 60)
    print(f"总案例数: {len(cases)}")
    print(f"分类变更: {len(changes)} 个")
    
    if changes:
        print("\n变更详情:")
        for change in changes:
            print(f"  - {change['name']}: {change['old']} → {change['new']}")
    
    print("\n注意: 重新分类后的数据已保存，请手动运行 readme_generator.py 更新 README.md")


if __name__ == '__main__':
    from dotenv import load_dotenv
    
    # 加载环境变量
    env_paths = [
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '.env'),
        '.env'
    ]
    for path in env_paths:
        if os.path.exists(path):
            load_dotenv(path)
            break
    
    reclassify_cases()
