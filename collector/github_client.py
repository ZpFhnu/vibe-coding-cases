"""
GitHub API 客户端 - 搜索和获取仓库信息
"""
import requests
import base64
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def search_repositories(self, query: str, per_page: int = 30) -> List[Dict]:
        """搜索仓库"""
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": per_page
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("items", [])
    
    def get_repository(self, owner: str, repo: str) -> Dict:
        """获取仓库详细信息"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """获取 README 内容"""
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        data = response.json()
        
        # 解码 base64 内容
        content = data.get("content", "")
        if content:
            try:
                return base64.b64decode(content).decode("utf-8")
            except:
                return None
        return None
    
    def get_file_structure(self, owner: str, repo: str, path: str = "") -> List[str]:
        """获取仓库文件结构"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return []
        
        items = response.json()
        files = []
        
        for item in items:
            if item["type"] == "file":
                files.append(item["path"])
            elif item["type"] == "dir" and path == "":
                # 只获取根目录下的文件夹名
                files.append(item["name"] + "/")
        
        return files
    
    def get_commits(self, owner: str, repo: str, per_page: int = 10) -> List[Dict]:
        """获取最近提交"""
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"per_page": per_page}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            return []
        
        return response.json()
    
    def search_vibe_coding_projects(self, min_stars: int = 5) -> List[Dict]:
        """
        搜索 vibe-coding 相关项目
        使用多个关键词组合搜索
        """
        search_queries = [
            # 英文关键词
            f'"vibe coding" in:readme stars:>{min_stars}',
            f'"vibe-coding" in:readme stars:>{min_stars}',
            f'"built with cursor" in:readme stars:>{min_stars}',
            f'"made with cursor" in:readme stars:>{min_stars}',
            f'"claude code" in:readme stars:>{min_stars}',
            f'"bolt.new" in:readme stars:>{min_stars}',
            f'"built with bolt" in:readme stars:>{min_stars}',
            f'"lovable" in:readme stars:>{min_stars}',
            f'"v0.dev" in:readme stars:>{min_stars}',
            f'"windsurf" in:readme stars:>{min_stars}',
            f'"trae" in:readme stars:>{min_stars}',
            # 中文关键词
            f'"AI生成" in:readme stars:>{min_stars}',
            f'"AI辅助" in:readme stars:>{min_stars}',
            f'"cursor开发" in:readme stars:>{min_stars}',
        ]
        
        all_repos = []
        seen_ids = set()
        
        for query in search_queries:
            try:
                repos = self.search_repositories(query, per_page=20)
                for repo in repos:
                    if repo["id"] not in seen_ids:
                        seen_ids.add(repo["id"])
                        all_repos.append(repo)
            except Exception as e:
                print(f"搜索失败 {query}: {e}")
                continue
        
        # 按 stars 排序
        all_repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        
        return all_repos
