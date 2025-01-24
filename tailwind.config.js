const defaultTheme = require("tailwindcss/defaultTheme")

module.exports = {
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
        green: '#43B166',
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
        selected: 'selected="true"', // data-selected:bg-white => element[data-selected]
        correct: 'correct="true"', // data-correct:bg-white => element[data-correct]
        wrong: 'wrong="true"', // data-wrong:bg-white => element[data-wrong]
        wrongSelected: 'wrong-selected="true"', // data-wrongSelected:bg-white => element[data-wrong-selected]
        correctSelected: 'correct-selected="true"', // data-correctSelected:bg-white => element[data-correct-selected]
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
  plugins: [
  ]
}
