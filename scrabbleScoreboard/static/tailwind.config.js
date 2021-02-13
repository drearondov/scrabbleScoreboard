module.exports = {
  purge: [
    './src/**/*.html',
    './src/**/*.js',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'light-green': '#B8BB26',
        'neutral-red': '#CC241D',
        'neutral-blue': '#458588',
        'bright-yellow': '#FABD2F',
        'neutral-orange': '#D65D03',
        'light-purple': '#D3869B'
      },
    },
    fontFamily: {
      'sans': ['Montserrat', 'sans-serif']
    }
  },
  variants: {
    extend: {},
  },
  plugins: [
  ],
}
