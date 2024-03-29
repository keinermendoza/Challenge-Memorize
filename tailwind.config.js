/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/templates/**/*.html",
    "./**/templates/**/partials/**/*.html",
    "./**/static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        darkbody : "#15022b",
        darkheader: "#2b1740",
        right: "#00ff00",
        wrong: "rgb(255, 99, 132)",
        yellow: "rgb(255, 205, 86)",
      },
      fontFamily: {
        bresse: ["bresse", "sans-serif"],
      },
      maxWidth: {
        '1440px': '1440px',
      },
      screens: {
        customMax:'1440px', 
      }
    },
  },
  plugins: [],
}

