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
    
    def search_repositories(self, query: str, per_page: int = 30, page: int = 1) -> List[Dict]:
        """搜索仓库，支持翻页"""
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": per_page,
            "page": page
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
    
    def search_vibe_coding_projects(self, min_stars: int = 5, processed_ids: set = None, 
                                     min_new_per_query: int = 5, max_pages: int = 10) -> List[Dict]:
        """
        搜索 vibe-coding 相关项目
        每个关键词至少找到 min_new_per_query 个未处理的项目才停止翻页
        
        Args:
            min_stars: 最小 stars 数
            processed_ids: 已处理的仓库 ID 集合
            min_new_per_query: 每个关键词至少找到的未处理项目数
            max_pages: 每个关键词最大翻页数
        """
        if processed_ids is None:
            processed_ids = set()
        
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
            f'"codeium" in:readme stars:>{min_stars}',
            f'"github copilot" in:readme stars:>{min_stars}',
            f'"ai generated" in:readme stars:>{min_stars}',
            f'"ai powered" in:readme stars:>{min_stars}',
            # 中文关键词
            f'"AI生成" in:readme stars:>{min_stars}',
            f'"AI辅助" in:readme stars:>{min_stars}',
            f'"cursor开发" in:readme stars:>{min_stars}',
            f'"AI编程" in:readme stars:>{min_stars}',
        ]
        
        all_new_repos = []
        seen_ids = set()  # 本次搜索已见的 ID（去重用）
        
        for query in search_queries:
            new_found_for_this_query = 0
            
            try:
                # 翻页获取，直到找到足够的新项目或翻完所有页
                for page in range(1, max_pages + 1):
                    repos = self.search_repositories(query, per_page=30, page=page)
                    
                    # 如果这一页没有结果，停止翻页
                    if not repos:
                        break
                    
                    for repo in repos:
                        repo_id = repo["id"]
                        
                        # 跳过本次搜索已见过的（去重）
                        if repo_id in seen_ids:
                            continue
                        seen_ids.add(repo_id)
                        
                        # 如果是未处理的，加入结果
                        if repo_id not in processed_ids:
                            all_new_repos.append(repo)
                            new_found_for_this_query += 1
                    
                    # 如果这一页没满，说明后面没有了
                    if len(repos) < 30:
                        break
                    
                    # 如果已经找到足够的新项目，停止翻页
                    if new_found_for_this_query >= min_new_per_query:
                        print(f"  关键词完成: 找到 {new_found_for_this_query} 个新项目")
                        break
                    
            except Exception as e:
                print(f"搜索失败 {query}: {e}")
                continue
        
        # 按 stars 排序
        all_new_repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        
        return all_new_repos
