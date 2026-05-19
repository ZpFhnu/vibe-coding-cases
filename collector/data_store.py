"""
数据存储模块 - 使用 JSON 文件存储
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class DataStore:
    """JSON 文件数据存储"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 默认存储到 web/data 目录，前端可以直接读取
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'web', 'data'
            )
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.cases_file = os.path.join(data_dir, 'cases.json')
        self.processed_file = os.path.join(data_dir, 'processed.json')
        self.stats_file = os.path.join(data_dir, 'stats.json')
    
    def load_cases(self) -> List[Dict]:
        """加载所有案例"""
        if not os.path.exists(self.cases_file):
            return []
        
        try:
            with open(self.cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('cases', [])
        except Exception as e:
            print(f"加载案例失败: {e}")
            return []
    
    def save_cases(self, cases: List[Dict]):
        """保存所有案例"""
        data = {
            'cases': cases,
            'updated_at': datetime.now().isoformat(),
            'total_count': len(cases)
        }
        
        with open(self.cases_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_case(self, case: Dict) -> bool:
        """添加新案例，如果已存在则更新"""
        cases = self.load_cases()
        
        # 检查是否已存在（通过 github_id 或 full_name）
        existing_idx = None
        for idx, c in enumerate(cases):
            if (c.get('github_id') == case.get('github_id') or 
                c.get('full_name') == case.get('full_name')):
                existing_idx = idx
                break
        
        # 添加元数据
        case['updated_at'] = datetime.now().isoformat()
        
        if existing_idx is not None:
            # 更新现有案例，保留创建时间
            case['created_at'] = cases[existing_idx].get('created_at', case['updated_at'])
            cases[existing_idx] = case
            print(f"更新案例: {case.get('full_name')}")
        else:
            # 添加新案例
            case['created_at'] = case['updated_at']
            cases.append(case)
            print(f"新增案例: {case.get('full_name')}")
        
        # 按 stars 排序
        cases.sort(key=lambda x: x.get('stars', 0), reverse=True)
        
        self.save_cases(cases)
        return existing_idx is None
    
    def get_processed_ids(self) -> set:
        """获取已处理的仓库 ID"""
        if not os.path.exists(self.processed_file):
            return set()
        
        try:
            with open(self.processed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('processed_ids', []))
        except:
            return set()
    
    def add_processed_id(self, repo_id: int):
        """添加已处理的仓库 ID"""
        processed_ids = self.get_processed_ids()
        processed_ids.add(repo_id)
        
        data = {
            'processed_ids': list(processed_ids),
            'updated_at': datetime.now().isoformat()
        }
        
        with open(self.processed_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        cases = self.load_cases()
        
        if not cases:
            return {
                'total': 0,
                'by_category': {},
                'by_ai_tool': {},
                'by_tech_stack': {},
                'last_updated': None
            }
        
        # 分类统计
        by_category = {}
        by_ai_tool = {}
        by_tech_stack = {}
        
        for case in cases:
            # 分类
            category = case.get('category', '其他')
            by_category[category] = by_category.get(category, 0) + 1
            
            # AI 工具
            for tool in case.get('ai_tools', []):
                by_ai_tool[tool] = by_ai_tool.get(tool, 0) + 1
            
            # 技术栈
            for tech in case.get('tech_stack', []):
                by_tech_stack[tech] = by_tech_stack.get(tech, 0) + 1
        
        # 读取更新时间
        updated_at = None
        if os.path.exists(self.cases_file):
            try:
                with open(self.cases_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    updated_at = data.get('updated_at')
            except:
                pass
        
        stats = {
            'total': len(cases),
            'by_category': by_category,
            'by_ai_tool': by_ai_tool,
            'by_tech_stack': by_tech_stack,
            'last_updated': updated_at
        }
        
        # 保存统计
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        return stats
    
    def case_exists(self, github_id: int = None, full_name: str = None) -> bool:
        """检查案例是否已存在"""
        cases = self.load_cases()
        
        for case in cases:
            if github_id and case.get('github_id') == github_id:
                return True
            if full_name and case.get('full_name') == full_name:
                return True
        
        return False
