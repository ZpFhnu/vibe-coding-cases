'use client'

import { useState } from 'react'

interface FilterBarProps {
  categories: string[]
}

const categoryEmojis: Record<string, string> = {
  'Web应用': '🌐',
  '移动端': '📱',
  '游戏': '🎮',
  '工具': '🛠️',
  'Chrome插件': '🔌',
  'VSCode插件': '📝',
  'CLI工具': '⌨️',
  '其他': '📦',
}

export default function FilterBar({ categories }: FilterBarProps) {
  const [activeFilter, setActiveFilter] = useState<string>('全部')
  
  const allCategories = ['全部', ...categories]

  return (
    <section className="bg-white border-b border-gray-200 sticky top-16 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        {/* Search Bar */}
        <div className="mb-4">
          <div className="relative max-w-md">
            <input
              type="text"
              placeholder="搜索项目、技术栈、AI工具..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <svg
              className="absolute left-3 top-2.5 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>

        {/* Category Filters */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
          <span className="text-sm text-gray-500 whitespace-nowrap mr-2">
            分类:
          </span>
          {allCategories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveFilter(category)}
              className={`px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                activeFilter === category
                  ? 'bg-primary-100 text-primary-700 border border-primary-200'
                  : 'bg-gray-100 text-gray-700 border border-gray-200 hover:bg-gray-200'
              }`}
            >
              {category !== '全部' && categoryEmojis[category]}
              {category}
            </button>
          ))}
        </div>
      </div>
    </section>
  )
}
