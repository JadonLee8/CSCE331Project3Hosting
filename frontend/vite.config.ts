import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [tailwindcss(), svelte()],
  server: {
    proxy: {
      '/api': loadEnv(mode, process.cwd(), 'VITE_').VITE_API_URL || 'http://localhost:8080',
    },
  },
}))
