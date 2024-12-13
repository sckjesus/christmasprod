const colors = require('tailwindcss/colors');

module.exports = {
  content: [
      "./templates/**/*.html", // Flask templates
      "./static/**/*.js", // JavaScript files
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.blue['600'], // Tailwind's blue-500 as primary
        'primary-light': colors.blue['500'], // Tailwind's blue-400 as hover color
        'primary-dark': colors.blue['700'], // Tailwind's blue-700 for dark mode
        secondary: colors.amber['600'], // Tailwind's amber-500 as secondary
        'secondary-light': colors.amber['500'], // Tailwind's amber-400 as hover
        'secondary-dark': colors.amber['700'], // Tailwind's amber-600 for dark mode
        neutral: {
          light: colors.gray['200'], // Tailwind's gray-200
          DEFAULT: colors.gray['500'], // Tailwind's gray-500
          dark: colors.gray['700'], // Tailwind's gray-700
        },
        success: {
          DEFAULT: colors.emerald['500'], // Tailwind's green-500
          'light': colors.emerald['400'], // Tailwind's green-500
          'dark': colors.emerald['600'], // Tailwind's green-500
        },
        warning: colors.yellow['500'], // Tailwind's yellow-500
        error: colors.red['500'], // Tailwind's red-500
        background: {
          light: colors.gray['100'], // Tailwind's gray-50 for light background
          dark: colors.gray['900'], // Tailwind's gray-900 for dark background
        },
        surface: {
          light: colors.white, // Tailwind's white
          dark: colors.gray['800'], // Tailwind's gray-800
        },
      },
    },
  },
  darkMode: 'class', // Enable class-based dark mode
  plugins: [],
};
