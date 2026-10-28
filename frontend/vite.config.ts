import { svelte } from '@sveltejs/vite-plugin-svelte'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    // Forward /api calls to the Go backend so the browser sees one origin (no CORS)
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
})
