/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fantasy: {
          dark: '#08071A',
          card: 'rgba(30, 41, 59, 0.65)',
          border: 'rgba(255, 255, 255, 0.09)',
          primary: '#6366F1',
          secondary: '#8B5CF6',
          accent: '#EC4899',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
      },
      backgroundImage: {
        'fantasy-gradient': 'radial-gradient(circle at 10% 20%, #17153B 0%, #0F1026 50%, #08071A 100%)',
        'title-gradient': 'linear-gradient(135deg, #FF6B6B 0%, #FF8E53 25%, #FFD93D 50%, #6BCB77 75%, #4D96FF 100%)',
      }
    },
  },
  plugins: [],
}
