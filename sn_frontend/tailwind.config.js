/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    extend: {
      zIndex: {
        '100': '100',
      },
      fontFamily: {
        title: ["Comfortaa", "sans-serif"],
        style: ["Indie Flower", "cursive"],
        normal: ["Kanit", "sans-serif"],
        succinct: ["Oswald", "sans-serif"],
      },
      rotate: {
        '270': '270deg',
      },
    },
    screens: {
      'xs': '320px',
      'xm': '444px',
      'sm': '640px',
      'md': '774px',
      'lm': '875px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    }
  },
  plugins: [
    require('tailwind-scrollbar')({ nocompatible: true }),
  ],
}

