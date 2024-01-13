/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html", "./**/templates/**/snipets/*.html"],
  theme: {
    extend: {
      colors: {
        darkbody : "#15022b",
        darkheader: "#2b1740",
      },
    },
  },
  plugins: [],
}

