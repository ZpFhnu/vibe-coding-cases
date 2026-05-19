/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'dist',
  images: {
    unoptimized: true,
  },
  // 为 GitHub Pages 配置基础路径
  // basePath: '/vibe-coding-cases',
  // assetPrefix: '/vibe-coding-cases',
}

module.exports = nextConfig
