import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		headers: {
			'access-control-allow-origin': '*',
			'access-control-allow-methods': 'GET, POST, PUT',
			'access-control-allow-headers': 'Content-Type',
			'access-control-allow-credentials': 'true'
		},
		proxy: {
			'/workers': {
				target: 'http://0.0.0.0:55555/',
				changeOrigin: true
			},
			'/buses': {
				target: 'http://0.0.0.0:55555/',
				changeOrigin: true
			},
			'/courses': {
				target: 'http://0.0.0.0:55555/',
				changeOrigin: true
			},
		}
	}
});
