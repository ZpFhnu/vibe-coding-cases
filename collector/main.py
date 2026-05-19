"""
主程序 - 自动收集 vibe-coding 项目
"""
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

from github_client import GitHubClient
from ai_analyzer import AIFactory
from data_store import DataStore
from readme_generator import generate_readme


def load_env():
    """加载环境变量"""
    # 尝试从多个位置加载 .env 文件
    env_paths = [
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '.env'),
        '.env'
    ]
    
    for path in env_paths:
        if os.path.exists(path):
            load_dotenv(path)
            print(f"已加载环境变量: {path}")
            break


def collect_projects():
    """收集项目主流程"""
    print("=" * 60)
    print(f"开始收集 vibe-coding 项目 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 初始化组件
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("错误: 请设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)
    
    github = GitHubClient(github_token)
    store = DataStore()
    
    # 创建 AI 分析器
    try:
        analyzer = AIFactory.create_analyzer()
        ai_provider = os.getenv('AI_PROVIDER', 'deepseek')
        print(f"使用 AI 提供商: {ai_provider}")
    except Exception as e:
        print(f"创建 AI 分析器失败: {e}")
        sys.exit(1)
    
    # 获取配置
    min_stars = int(os.getenv('MIN_STARS', '5'))
    max_projects = int(os.getenv('MAX_PROJECTS_PER_RUN', '30'))
    min_confidence = float(os.getenv('MIN_CONFIDENCE', '0.75'))
    min_quality = int(os.getenv('MIN_QUALITY', '6'))
    
    print(f"配置: min_stars={min_stars}, max_projects={max_projects}, "
          f"min_confidence={min_confidence}, min_quality={min_quality}")
    
    # 获取已处理的项目 ID
    processed_ids = store.get_processed_ids()
    print(f"已处理项目数: {len(processed_ids)}")
    
    # 搜索项目（传入 processed_ids，在搜索时就过滤）
    print("\n正在搜索 GitHub 项目...")
    repos = github.search_vibe_coding_projects(
        min_stars=min_stars,
        processed_ids=processed_ids,
        min_new_per_query=5,  # 每个关键词至少找 5 个新的
        max_pages=10
    )
    print(f"找到 {len(repos)} 个未处理的候选项目")
    
    new_repos = repos  # 已经过滤过了
    
    # 限制处理数量为 50
    max_projects = 50
    repos_to_process = new_repos[:max_projects]
    print(f"本次将处理前 {len(repos_to_process)} 个项目\n")
    
    # 统计
    stats = {
        'total': len(repos_to_process),
        'success': 0,
        'failed': 0,
        'accepted': 0,
        'rejected': 0
    }
    
    # 处理每个项目
    for idx, repo in enumerate(repos_to_process, 1):
        repo_name = repo['full_name']
        print(f"\n[{idx}/{len(repos_to_process)}] 处理: {repo_name}")
        print("-" * 40)
        
        try:
            # 获取详细信息
            owner, repo_name_only = repo_name.split('/')
            
            print("  获取 README...")
            readme = github.get_readme(owner, repo_name_only)
            
            print("  获取文件结构...")
            file_structure = github.get_file_structure(owner, repo_name_only)
            
            print("  获取提交记录...")
            commits = github.get_commits(owner, repo_name_only)
            
            # 准备分析数据
            repo_data = {
                'id': repo['id'],
                'full_name': repo_name,
                'description': repo.get('description', ''),
                'language': repo.get('language'),
                'stargazers_count': repo.get('stargazers_count', 0),
                'forks_count': repo.get('forks_count', 0),
                'html_url': repo['html_url'],
                'homepage': repo.get('homepage'),
                'created_at': repo.get('created_at'),
                'pushed_at': repo.get('pushed_at'),
                'readme': readme,
                'file_structure': file_structure,
                'recent_commits': commits
            }
            
            # AI 分析
            print("  AI 分析中...")
            analysis = analyzer.analyze_project(repo_data)
            
            print(f"  结果: is_vibe_coding={analysis['is_vibe_coding']}, "
                  f"confidence={analysis['confidence']:.2f}, "
                  f"quality={analysis['quality_score']}")
            
            # 质量检查
            if not analysis['is_vibe_coding']:
                print(f"  ❌ 拒绝: 不是 vibe-coding 项目")
                stats['rejected'] += 1
            elif analysis['confidence'] < min_confidence:
                print(f"  ❌ 拒绝: 置信度太低 ({analysis['confidence']:.2f} < {min_confidence})")
                stats['rejected'] += 1
            elif analysis['quality_score'] < min_quality:
                print(f"  ❌ 拒绝: 质量分太低 ({analysis['quality_score']} < {min_quality})")
                stats['rejected'] += 1
            else:
                # 通过检查，保存案例
                case = {
                    'github_id': repo['id'],
                    'full_name': repo_name,
                    'name': repo_name_only,
                    'owner': owner,
                    'description': repo.get('description', ''),
                    'chinese_description': analysis['chinese_description'],
                    'english_description': analysis.get('english_description', ''),
                    'html_url': repo['html_url'],
                    'homepage': analysis.get('demo_url') or repo.get('homepage'),
                    'language': repo.get('language'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'ai_tools': analysis['ai_tools'],
                    'tech_stack': analysis['tech_stack'],
                    'category': analysis['category'],
                    'created_at': repo.get('created_at', ''),
                    'pushed_at': repo.get('pushed_at', ''),
                    'quality_score': analysis['quality_score'],
                    'confidence': analysis['confidence'],
                    'why_vibe_coding': analysis['why_vibe_coding'],
                    'readme_preview': readme[:500] if readme else None
                }
                
                is_new = store.add_case(case)
                print(f"  ✅ 接受: {'新增' if is_new else '更新'}案例")
                stats['accepted'] += 1
            
            # 标记为已处理
            store.add_processed_id(repo['id'])
            stats['success'] += 1
            
            # 延迟，避免 API 限制
            time.sleep(1)
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            stats['failed'] += 1
            # 仍然标记为已处理，避免重复处理有问题的项目
            store.add_processed_id(repo['id'])
            continue
    
    # 更新统计
    store.get_stats()
    
    # 重新生成 README.md
    print("\n生成 README.md...")
    cases = store.load_cases()
    generate_readme(cases)
    
    # 打印总结
    print("\n" + "=" * 60)
    print("收集完成!")
    print("=" * 60)
    print(f"总计处理: {stats['total']}")
    print(f"成功: {stats['success']}")
    print(f"失败: {stats['failed']}")
    print(f"接受: {stats['accepted']}")
    print(f"拒绝: {stats['rejected']}")
    print(f"当前案例库总数: {len(store.load_cases())}")
    print("=" * 60)


def main():
    """主入口"""
    load_env()
    
    try:
        collect_projects()
    except KeyboardInterrupt:
        print("\n用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
