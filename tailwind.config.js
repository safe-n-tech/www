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
        primary: '#153e60',
        secondary: '#153e60',
        green: '#1C4A2B',
        orange: '#DC8930',
        red: '#CF4339',
        tertiary: '#89D0FF',
        dark_gray: '#081926',
        gray: '#000000',
        light_gray: '#F6F5F5',
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
