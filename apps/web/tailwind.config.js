/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#edf5f3',
          100: '#d8eae5',
          500: '#2d7480',
          600: '#1d5c68',
          700: '#154b56',
          900: '#0a3039',
        }
      }
    }
  },
  plugins: [],
}
