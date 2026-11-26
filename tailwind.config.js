/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4a78c2',
        secondary: '#6a7587',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light', 'dark'],
    darkMode: ['selector', '[data-tema="oscuro"]'],
  },
}
