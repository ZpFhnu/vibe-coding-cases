import fs from 'fs'
import path from 'path'

export interface Case {
  github_id: number
  full_name: string
  name: string
  owner: string
  description: string
  chinese_description: string
  html_url: string
  homepage?: string
  language?: string
  stars: number
  forks: number
  ai_tools: string[]
  tech_stack: string[]
  category: string
  estimated_hours: string
  quality_score: number
  confidence: number
  why_vibe_coding: string
  readme_preview?: string
  created_at: string
  updated_at: string
}

export interface Stats {
  total: number
  by_category: Record<string, number>
  by_ai_tool: Record<string, number>
  by_tech_stack: Record<string, number>
  last_updated?: string
}

export function loadCases(): Case[] {
  try {
    const dataPath = path.join(process.cwd(), 'data', 'cases.json')
    
    if (!fs.existsSync(dataPath)) {
      return []
    }
    
    const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'))
    return data.cases || []
  } catch (error) {
    console.error('加载案例失败:', error)
    return []
  }
}

export function getCategories(): string[] {
  const cases = loadCases()
  const categories = new Set<string>()
  
  cases.forEach(c => {
    if (c.category) {
      categories.add(c.category)
    }
  })
  
  return Array.from(categories).sort()
}

export function getStats(): Stats {
  try {
    const statsPath = path.join(process.cwd(), 'data', 'stats.json')
    
    if (!fs.existsSync(statsPath)) {
      // 实时计算统计
      return calculateStats()
    }
    
    return JSON.parse(fs.readFileSync(statsPath, 'utf-8'))
  } catch (error) {
    return calculateStats()
  }
}

function calculateStats(): Stats {
  const cases = loadCases()
  
  const by_category: Record<string, number> = {}
  const by_ai_tool: Record<string, number> = {}
  const by_tech_stack: Record<string, number> = {}
  
  cases.forEach(c => {
    // 分类统计
    const cat = c.category || '其他'
    by_category[cat] = (by_category[cat] || 0) + 1
    
    // AI 工具统计
    c.ai_tools?.forEach(tool => {
      by_ai_tool[tool] = (by_ai_tool[tool] || 0) + 1
    })
    
    // 技术栈统计
    c.tech_stack?.forEach(tech => {
      by_tech_stack[tech] = (by_tech_stack[tech] || 0) + 1
    })
  })
  
  return {
    total: cases.length,
    by_category,
    by_ai_tool,
    by_tech_stack
  }
}

export function getCasesByCategory(category: string): Case[] {
  const cases = loadCases()
  return cases.filter(c => c.category === category)
}

export function getCasesByAiTool(tool: string): Case[] {
  const cases = loadCases()
  return cases.filter(c => c.ai_tools?.includes(tool))
}

export function searchCases(query: string): Case[] {
  const cases = loadCases()
  const lowerQuery = query.toLowerCase()
  
  return cases.filter(c => 
    c.name?.toLowerCase().includes(lowerQuery) ||
    c.description?.toLowerCase().includes(lowerQuery) ||
    c.chinese_description?.toLowerCase().includes(lowerQuery) ||
    c.tech_stack?.some(t => t.toLowerCase().includes(lowerQuery)) ||
    c.ai_tools?.some(t => t.toLowerCase().includes(lowerQuery))
  )
}
