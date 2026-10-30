import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), svelte()],
  server: {
    // Forward /api calls to the Go backend so the browser sees one origin (no CORS)
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
})
