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
        primary: '#2FA2EE',
        secondary: '#0155CE',
        orange: '#BB2626',
        green: '#13a039',
        tertiary: '#89D0FF',
        dark_gray: '#4A4A52',
        gray: '#AAAAAA',
        light_gray: '#F9F9F9',
        white: '#FFFFFF',
        light_white : '#F5F7FA',
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
      sans: ['Marianne', ...defaultTheme.fontFamily.sans],
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
