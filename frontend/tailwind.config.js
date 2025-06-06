/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',        // Memindai semua file HTML di ../templates
    './src/**/*.{js,jsx,ts,tsx}',    // Memindai semua file JS/TS di src/
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
