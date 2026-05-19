import { Case } from '../lib/data'

interface CaseCardProps {
  caseData: Case
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

const languageColors: Record<string, string> = {
  'JavaScript': 'bg-yellow-100 text-yellow-800',
  'TypeScript': 'bg-blue-100 text-blue-800',
  'Python': 'bg-green-100 text-green-800',
  'Go': 'bg-cyan-100 text-cyan-800',
  'Rust': 'bg-orange-100 text-orange-800',
  'Java': 'bg-red-100 text-red-800',
  'Vue': 'bg-emerald-100 text-emerald-800',
  'HTML': 'bg-orange-100 text-orange-800',
  'CSS': 'bg-blue-100 text-blue-800',
}

export default function CaseCard({ caseData }: CaseCardProps) {
  const {
    name,
    full_name,
    chinese_description,
    description,
    html_url,
    homepage,
    language,
    stars,
    forks,
    ai_tools,
    tech_stack,
    category,
    estimated_hours,
    quality_score,
  } = caseData

  // 格式化数字
  const formatNumber = (num: number): string => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k'
    }
    return num.toString()
  }

  // 获取分类 emoji
  const categoryEmoji = categoryEmojis[category] || '📦'

  // 获取语言颜色
  const languageColor = languageColors[language || ''] || 'bg-gray-100 text-gray-800'

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-200">
      {/* Card Header */}
      <div className="p-5">
        {/* Category & Quality Badge */}
        <div className="flex items-center justify-between mb-3">
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
            {categoryEmoji} {category}
          </span>
          {quality_score >= 8 && (
            <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700">
              ⭐ 精选
            </span>
          )}
        </div>

        {/* Title */}
        <h3 className="font-bold text-lg text-gray-900 mb-2 line-clamp-1" title={name}>
          {name}
        </h3>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2 h-10">
          {chinese_description || description || '暂无描述'}
        </p>

        {/* Stats */}
        <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
          <span className="flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            {formatNumber(stars)}
          </span>
          {forks > 0 && (
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              {formatNumber(forks)}
            </span>
          )}
          {language && (
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${languageColor}`}>
              {language}
            </span>
          )}
        </div>

        {/* AI Tools */}
        {ai_tools && ai_tools.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-3">
            {ai_tools.slice(0, 3).map((tool) => (
              <span
                key={tool}
                className="px-2 py-1 rounded-md text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100"
              >
                🤖 {tool}
              </span>
            ))}
            {ai_tools.length > 3 && (
              <span className="px-2 py-1 rounded-md text-xs text-gray-500">
                +{ai_tools.length - 3}
              </span>
            )}
          </div>
        )}

        {/* Tech Stack */}
        {tech_stack && tech_stack.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {tech_stack.slice(0, 4).map((tech) => (
              <span
                key={tech}
                className="px-2 py-1 rounded-md text-xs text-gray-600 bg-gray-50 border border-gray-200"
              >
                {tech}
              </span>
            ))}
            {tech_stack.length > 4 && (
              <span className="px-2 py-1 text-xs text-gray-400">
                +{tech_stack.length - 4}
              </span>
            )}
          </div>
        )}

        {/* Estimated Time */}
        {estimated_hours && (
          <div className="flex items-center gap-1 text-xs text-gray-500 mb-4">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            开发时长: {estimated_hours}
          </div>
        )}
      </div>

      {/* Card Footer - Actions */}
      <div className="px-5 py-4 bg-gray-50 border-t border-gray-100 flex items-center gap-3">
        <a
          href={html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          源码
        </a>
        {homepage && (
          <a
            href={homepage}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
            演示
          </a>
        )}
      </div>
    </div>
  )
}
