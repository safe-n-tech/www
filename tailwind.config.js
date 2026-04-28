const defaultTheme = require("tailwindcss/defaultTheme")

module.exports = {
  darkMode: 'class',
  content: [
    "./themes/**/layouts/**/*.html",
    "./content/**/layouts/**/*.html",
    "./layouts/**/*.html",
    "./content/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0449B8',
        secondary: '#153E60',
        tertiary: '#89D0FF',
        green: '#1C4A2B',
        orange: '#DC8930',
        red: '#CF4339',
        light_gray: '#F6F5F5',
        gray: '#E0E0E0',
        dark_gray: '#424242',
        white: '#FFFFFF',
        light_white: '#F5F7FA',
        black: '#000000',
      },
      data: {
        selected: 'selected="true"',
        correct: 'correct="true"',
        wrong: 'wrong="true"',
        wrongSelected: 'wrong-selected="true"',
        correctSelected: 'correct-selected="true"',
      },
    },
    fontFamily: {
      sans: ['Arial', 'sans-serif'],
      display: ['Montserrat']
    },
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '8rem',
        '2xl': '12rem',
      },
    },
  },
  plugins: []
}
