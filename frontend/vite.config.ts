import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Base path for GitHub Pages: /PDD/ (repository name)
const base = process.env.VITE_BASE_URL || '/PDD/'

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:5000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom') || id.includes('react-router')) return 'vendor'
            if (id.includes('framer-motion')) return 'framer'
            if (id.includes('recharts')) return 'charts'
            if (id.includes('three') || id.includes('@react-three')) return 'three'
          }
        },
      },
    },
  },
})
