import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/data': {
        target: 'http://127.0.0.1:5000/api/data',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/data/, ''),
      },
      '/api/get': {
        target: 'http://127.0.0.1:5000/api/get',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/get/, ''),
      },
      '/api/messages': {
        target: 'http://127.0.0.1:5000/api/messages',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/messages/, ''),
      },
    },
  },
})

