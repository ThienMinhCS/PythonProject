/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        airline: {
          navy: '#0A1E3C',
          blue: '#1A5276',
          lightblue: '#D4E6F1',
          gold: '#F1C40F',
          red: '#E74C3C',
          dark: '#0D1B2A',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}