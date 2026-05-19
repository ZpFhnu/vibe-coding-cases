"""
为已有案例添加英文描述
一次性脚本，运行后给所有案例补 english_description
"""
import json
import os
from datetime import datetime
from ai_analyzer import AIFactory
from data_store import DataStore


def add_english_descriptions():
    """为已有案例添加英文描述"""
    print("=" * 60)
    print("开始为已有案例添加英文描述")
    print("=" * 60)
    
    store = DataStore()
    cases = store.load_cases()
    
    if not cases:
        print("没有案例需要处理")
        return
    
    # 筛选出没有英文描述的案例
    cases_need_english = [c for c in cases if not c.get('english_description')]
    
    print(f"共 {len(cases)} 个案例，其中 {len(cases_need_english)} 个需要添加英文描述")
    
    if not cases_need_english:
        print("所有案例已有英文描述，无需处理")
        return
    
    # 创建 AI 分析器
    try:
        analyzer = AIFactory.create_analyzer()
    except Exception as e:
        print(f"创建 AI 分析器失败: {e}")
        return
    
    # 统计
    success_count = 0
    failed_count = 0
    
    for idx, case in enumerate(cases_need_english, 1):
        print(f"\n[{idx}/{len(cases_need_english)}] 处理: {case.get('full_name', 'Unknown')}")
        
        # 准备数据
        repo_data = {
            'id': case.get('github_id'),
            'full_name': case.get('full_name'),
            'description': case.get('description', ''),
            'chinese_description': case.get('chinese_description', ''),
            'language': case.get('language'),
            'readme': case.get('readme_preview', ''),
        }
        
        try:
            # 调用 AI 生成英文描述
            english_desc = generate_english_description(analyzer, repo_data)
            
            if english_desc:
                case['english_description'] = english_desc
                case['updated_at'] = datetime.now().isoformat()
                success_count += 1
                print(f"  ✅ 成功: {english_desc[:60]}...")
            else:
                failed_count += 1
                print(f"  ❌ 生成失败")
                
        except Exception as e:
            failed_count += 1
            print(f"  ❌ 错误: {e}")
            continue
    
    # 保存更新后的数据
    store.save_cases(cases)
    
    # 打印总结
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)
    print(f"总案例数: {len(cases)}")
    print(f"成功添加: {success_count}")
    print(f"失败: {failed_count}")
    print("\n注意: 数据已保存，请运行 readme_generator.py 更新 README")


def generate_english_description(analyzer, repo_data: dict) -> str:
    """生成英文描述"""
    import requests
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    base_url = "https://api.deepseek.com"
    model = "deepseek-chat"
    
    prompt = f"""Please write a one-sentence English description for this project.

Project Name: {repo_data['full_name']}
Chinese Description: {repo_data.get('chinese_description', '')}
Original Description: {repo_data.get('description', '')}

Requirements:
- One sentence only
- Describe what the project does (not what technology it uses)
- Clear and concise
- Suitable for a README listing

Output format: Just the description sentence, nothing else."""

    response = requests.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 200
        },
        timeout=30
    )
    
    response.raise_for_status()
    result = response.json()
    content = result['choices'][0]['message']['content'].strip()
    
    # 清理可能的引号
    content = content.strip('"').strip("'")
    
    return content


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
    
    add_english_descriptions()
