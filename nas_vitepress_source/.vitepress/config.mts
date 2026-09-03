import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Jun's Wiki",
  description: 'AI × Quant × Media — 知識庫',
  lang: 'zh-Hant',
  cleanUrls: true,

  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
  },

  themeConfig: {
    nav: [
      { text: '首頁', link: '/' },
      { text: 'GitHub', link: 'https://github.com/Jnocode/wiki' },
    ],

    sidebar: [
      { text: '📖 知識庫本身', items: [
        { text: 'Knowledge Base 說明', link: '/entities/knowledge-base' },
        { text: 'MCP 配置說明', link: '/entities/mcp-config' },
      ]},
      { text: '🎓 學習', items: [
        { text: '工業工程課程', link: '/entities/ie-department' },
        { text: '書籍筆記', link: '/entities/book-notes' },
      ]},
      { text: '🛠 技術', items: [
        { text: 'Stable Diffusion 設定', link: '/concepts/stable-diffusion-setup' },
      ]},
      { text: '💼 專案', items: [
        { text: 'AI 內容商業模式', link: '/entities/ai-content-business' },
        { text: 'AI_Park 工作區', link: '/entities/ai-park-workspace' },
      ]},
      { text: '🎙 自媒體', items: [
        { text: '內容產出與除錯', link: '/entities/self-media' },
      ]},
      { text: '🔧 系統', items: [
        { text: 'WSL/Windows 部署', link: '/entities/hybrid-deployment' },
      ]},
      { text: '🎨 創意', items: [
        { text: '歌詞與隨筆', link: '/entities/creative-works' },
      ]},
    ],

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜尋', buttonAriaLabel: '搜尋知識庫' },
              modal: { noResultsText: '無結果', resetButtonTitle: '清除' },
            },
          },
        },
      },
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Jnocode/wiki' },
    ],
  },
})
