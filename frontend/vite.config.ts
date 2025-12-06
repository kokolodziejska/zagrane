import path from 'path';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// ten plik działa w KONTENERZE frontendu.
// Backend ma nazwę usługi 'backend' z docker-compose, port 8000.
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://backend:8000', // <- nazwa usługi z docker-compose
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
