import CaseCard from './components/CaseCard'
import FilterBar from './components/FilterBar'
import Header from './components/Header'
import { loadCases, getCategories, getStats } from './lib/data'

export default function Home() {
  const cases = loadCases()
  const categories = getCategories()
  const stats = getStats()

  return (
    <main className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              🧠 Vibe-Coding 案例库
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              发现用 AI 辅助编程开发的优秀项目，看看别人怎么用 AI 写代码
            </p>
            <div className="mt-6 flex justify-center gap-6 text-sm text-gray-500">
              <span>📦 {stats.total} 个案例</span>
              <span>🤖 {Object.keys(stats.by_ai_tool).length} 种 AI 工具</span>
              <span>🛠️ {Object.keys(stats.by_tech_stack).length} 种技术栈</span>
            </div>
          </div>
        </div>
      </section>

      {/* Filter Bar */}
      <FilterBar categories={categories} />

      {/* Cases Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {cases.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">📭</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">暂无案例</h3>
            <p className="text-gray-500">案例正在收集中，请稍后再来...</p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">
                🔥 热门案例
              </h2>
              <span className="text-sm text-gray-500">
                共 {cases.length} 个项目
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {cases.map((caseItem) => (
                <CaseCard key={caseItem.github_id} caseData={caseItem} />
              ))}
            </div>
          </>
        )}
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-500">
              © 2025 Vibe-Coding 案例库 - 自动收集 GitHub 上的 AI 编程项目
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-500 hover:text-gray-900"
              >
                GitHub
              </a>
              <a
                href="#"
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                提交案例 →
              </a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
