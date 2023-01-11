module.exports = {
  content: [
    "./themes/**/layouts/**/*.html",
    "./content/**/layouts/**/*.html",
    "./layouts/**/*.html",
    "./content/**/*.html"
  ],
  theme: {
    extends: {
    },
    colors: {
      primary: 'black',
      secondary: 'white',
    },
    fontFamily: {
      sans: ['Hind'],
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
