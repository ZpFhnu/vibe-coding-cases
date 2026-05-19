"""
AI 分析模块 - 使用国产 AI API 分析项目
支持: DeepSeek, 智谱, 通义千问, Kimi
"""
import json
import os
import re
from typing import Dict, Optional
import requests


class AIFactory:
    """AI 分析器工厂"""
    
    @staticmethod
    def create_analyzer(provider: Optional[str] = None):
        if provider is None:
            provider = os.getenv('AI_PROVIDER', 'deepseek').lower()
        
        analyzers = {
            'deepseek': DeepSeekAnalyzer,
            'zhipu': ZhipuAnalyzer,
            'qwen': QwenAnalyzer,
            'kimi': KimiAnalyzer,
        }
        
        analyzer_class = analyzers.get(provider)
        if analyzer_class is None:
            raise ValueError(f"不支持的 AI 提供商: {provider}")
        
        return analyzer_class()


class BaseAnalyzer:
    """分析器基类"""
    
    def extract_json_from_text(self, text: str) -> Optional[Dict]:
        """从文本中提取 JSON"""
        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            pass
        
        # 尝试提取 ```json 代码块
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # 尝试提取 { } 包裹的内容
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        return None


class DeepSeekAnalyzer(BaseAnalyzer):
    """DeepSeek API 分析器 - 推荐，性价比高"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        self.base_url = "https://api.deepseek.com"
        self.model = "deepseek-chat"
    
    def analyze_project(self, repo_data: Dict) -> Dict:
        """分析仓库是否为 vibe-coding 项目"""
        
        prompt = self._build_prompt(repo_data)
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 1500
            },
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # 解析 JSON
        parsed = self.extract_json_from_text(content)
        if parsed is None:
            raise ValueError(f"无法解析 AI 响应: {content[:200]}")
        
        return self._normalize_result(parsed, repo_data)
    
    def _build_prompt(self, repo_data: Dict) -> str:
        """构建分析 Prompt"""
        
        # 截取 README 前 3000 字符
        readme = repo_data.get('readme', '')[:3000] if repo_data.get('readme') else '无 README'
        
        # 文件结构
        files = repo_data.get('file_structure', [])
        file_structure = ', '.join(files[:20]) if files else '无法获取'
        
        # 最近提交信息
        commits = repo_data.get('recent_commits', [])
        commit_info = ''
        if commits:
            commit_info = '\n'.join([
                f"- {c.get('commit', {}).get('message', '')[:50]}"
                for c in commits[:5]
            ])
        
        return f"""请分析以下 GitHub 仓库，判断它是否是使用 AI 辅助编程（vibe-coding）方式开发的项目。

【仓库信息】
- 名称: {repo_data.get('full_name', 'Unknown')}
- 描述: {repo_data.get('description', '无描述')}
- 主要语言: {repo_data.get('language', 'Unknown')}
- Stars: {repo_data.get('stargazers_count', 0)}
- 创建时间: {repo_data.get('created_at', 'Unknown')}
- 更新时间: {repo_data.get('pushed_at', 'Unknown')}

【README 内容】（前3000字符）
{readme}

【文件结构】
{file_structure}

【最近提交】
{commit_info}

请输出以下 JSON 格式的分析结果：
{{
    "is_vibe_coding": true/false,
    "confidence": 0.0-1.0,
    "ai_tools": ["使用的AI工具，如: Cursor", "Claude", "v0", "Bolt", "Lovable", "Windsurf", "Trae", "Copilot", "Codeium", "通义灵码", "CodeGeeX"],
    "tech_stack": ["技术栈，如: React", "Vue", "Python", "Node.js", "Next.js", "TypeScript"],
    "category": "项目类型: Web应用/工具/游戏/移动端/Chrome插件/VSCode插件/CLI工具/其他",
    "estimated_hours": "估算开发时间: 1-5小时/半天/1-2天/一周/不确定",
    "chinese_description": "用一句话中文描述这个项目是做什么的",
    "quality_score": 1-10,
    "demo_url": "演示链接(从README中提取)或null",
    "why_vibe_coding": "判断理由，中文说明"
}}

判断标准：
1. README 中明确提到使用 AI 工具开发
2. 项目描述中有 "vibe coding", "AI generated", "built with Cursor" 等关键词
3. 项目结构简单，可能是快速原型
4. 提交信息中提到 AI 辅助

请只输出 JSON，不要其他内容。"""
    
    def _normalize_result(self, result: Dict, repo_data: Dict) -> Dict:
        """规范化结果"""
        # 确保必要字段存在
        normalized = {
            'is_vibe_coding': result.get('is_vibe_coding', False),
            'confidence': float(result.get('confidence', 0)),
            'ai_tools': result.get('ai_tools', []),
            'tech_stack': result.get('tech_stack', []),
            'category': result.get('category', '其他'),
            'estimated_hours': result.get('estimated_hours', '不确定'),
            'chinese_description': result.get('chinese_description', repo_data.get('description', '')),
            'quality_score': int(result.get('quality_score', 5)),
            'demo_url': result.get('demo_url'),
            'why_vibe_coding': result.get('why_vibe_coding', ''),
        }
        return normalized


class ZhipuAnalyzer(BaseAnalyzer):
    """智谱 GLM-4 分析器"""
    
    def __init__(self):
        self.api_key = os.getenv('ZHIPU_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 ZHIPU_API_KEY 环境变量")
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.model = "glm-4"
    
    def analyze_project(self, repo_data: Dict) -> Dict:
        try:
            from zhipuai import ZhipuAI
        except ImportError:
            raise ImportError("请安装 zhipuai: pip install zhipuai")
        
        client = ZhipuAI(api_key=self.api_key)
        
        prompt = self._build_prompt(repo_data)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        parsed = self.extract_json_from_text(content)
        
        if parsed is None:
            raise ValueError(f"无法解析 AI 响应: {content[:200]}")
        
        return self._normalize_result(parsed, repo_data)
    
    def _build_prompt(self, repo_data: Dict) -> str:
        # 简化版 prompt
        readme = repo_data.get('readme', '')[:2500] if repo_data.get('readme') else '无 README'
        return f"""分析GitHub仓库是否为vibe-coding项目。

仓库: {repo_data.get('full_name')}
描述: {repo_data.get('description', '无')}
README: {readme}

输出JSON格式:
{{
    "is_vibe_coding": bool,
    "confidence": float,
    "ai_tools": list,
    "tech_stack": list,
    "category": str,
    "estimated_hours": str,
    "chinese_description": str,
    "quality_score": int,
    "demo_url": str或null,
    "why_vibe_coding": str
}}"""
    
    def _normalize_result(self, result: Dict, repo_data: Dict) -> Dict:
        return {
            'is_vibe_coding': result.get('is_vibe_coding', False),
            'confidence': float(result.get('confidence', 0)),
            'ai_tools': result.get('ai_tools', []),
            'tech_stack': result.get('tech_stack', []),
            'category': result.get('category', '其他'),
            'estimated_hours': result.get('estimated_hours', '不确定'),
            'chinese_description': result.get('chinese_description', repo_data.get('description', '')),
            'quality_score': int(result.get('quality_score', 5)),
            'demo_url': result.get('demo_url'),
            'why_vibe_coding': result.get('why_vibe_coding', ''),
        }


class QwenAnalyzer(BaseAnalyzer):
    """通义千问分析器"""
    
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        self.model = "qwen-max"
    
    def analyze_project(self, repo_data: Dict) -> Dict:
        prompt = self._build_prompt(repo_data)
        
        response = requests.post(
            f"{self.base_url}/services/aigc/text-generation/generation",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "input": {"messages": [{"role": "user", "content": prompt}]},
                "parameters": {"result_format": "message", "temperature": 0.1}
            },
            timeout=60
        )
        
        response.raise_for_status()
        content = response.json()['output']['choices'][0]['message']['content']
        
        parsed = self.extract_json_from_text(content)
        if parsed is None:
            raise ValueError(f"无法解析 AI 响应: {content[:200]}")
        
        return self._normalize_result(parsed, repo_data)
    
    def _build_prompt(self, repo_data: Dict) -> str:
        readme = repo_data.get('readme', '')[:2500] if repo_data.get('readme') else '无 README'
        return f"""分析GitHub项目: {repo_data.get('full_name')}

README: {readme}

判断是否为vibe-coding项目，输出JSON:
{{
    "is_vibe_coding": bool,
    "confidence": float,
    "ai_tools": list,
    "tech_stack": list,
    "category": str,
    "chinese_description": str,
    "quality_score": int,
    "demo_url": str或null,
    "why_vibe_coding": str
}}"""
    
    def _normalize_result(self, result: Dict, repo_data: Dict) -> Dict:
        return {
            'is_vibe_coding': result.get('is_vibe_coding', False),
            'confidence': float(result.get('confidence', 0)),
            'ai_tools': result.get('ai_tools', []),
            'tech_stack': result.get('tech_stack', []),
            'category': result.get('category', '其他'),
            'estimated_hours': result.get('estimated_hours', '不确定'),
            'chinese_description': result.get('chinese_description', repo_data.get('description', '')),
            'quality_score': int(result.get('quality_score', 5)),
            'demo_url': result.get('demo_url'),
            'why_vibe_coding': result.get('why_vibe_coding', ''),
        }


class KimiAnalyzer(BaseAnalyzer):
    """Moonshot Kimi 分析器"""
    
    def __init__(self):
        self.api_key = os.getenv('MOONSHOT_API_KEY')
        if not self.api_key:
            raise ValueError("请设置 MOONSHOT_API_KEY 环境变量")
        self.base_url = "https://api.moonshot.cn/v1"
        self.model = "moonshot-v1-8k"
    
    def analyze_project(self, repo_data: Dict) -> Dict:
        prompt = self._build_prompt(repo_data)
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            },
            timeout=60
        )
        
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        parsed = self.extract_json_from_text(content)
        if parsed is None:
            raise ValueError(f"无法解析 AI 响应: {content[:200]}")
        
        return self._normalize_result(parsed, repo_data)
    
    def _build_prompt(self, repo_data: Dict) -> str:
        readme = repo_data.get('readme', '')[:2500] if repo_data.get('readme') else '无 README'
        return f"""分析GitHub仓库: {repo_data.get('full_name')}

README内容:
{readme}

判断是否为vibe-coding项目，输出JSON格式:
{{
    "is_vibe_coding": bool,
    "confidence": float,
    "ai_tools": list,
    "tech_stack": list,
    "category": str,
    "estimated_hours": str,
    "chinese_description": str,
    "quality_score": int,
    "demo_url": str或null,
    "why_vibe_coding": str
}}"""
    
    def _normalize_result(self, result: Dict, repo_data: Dict) -> Dict:
        return {
            'is_vibe_coding': result.get('is_vibe_coding', False),
            'confidence': float(result.get('confidence', 0)),
            'ai_tools': result.get('ai_tools', []),
            'tech_stack': result.get('tech_stack', []),
            'category': result.get('category', '其他'),
            'estimated_hours': result.get('estimated_hours', '不确定'),
            'chinese_description': result.get('chinese_description', repo_data.get('description', '')),
            'quality_score': int(result.get('quality_score', 5)),
            'demo_url': result.get('demo_url'),
            'why_vibe_coding': result.get('why_vibe_coding', ''),
        }
