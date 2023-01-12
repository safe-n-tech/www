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
        dark_gray: '#4A4A52',
        gray:'#AAAAAA',
        light_gray:'#F9F9F9',
        white:'#FFFFFF',
      },
    },
    colors: {
      primary: '#2FA2EE',
      secondary: '#0155CE',
      dark_gray: '#4A4A52',
      gray:'#AAAAAA',
      white:'#FFFFFF',
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
