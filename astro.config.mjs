import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://danielzheng1986726.github.io',
  base: '/',
  output: 'static',
  trailingSlash: 'always',
  redirects: { '/videos/': '/talks/' },
});
