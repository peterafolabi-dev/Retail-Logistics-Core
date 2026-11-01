// The repo has two Tailwind configs: tailwind.config.js builds the Django
// templates' CSS, tailwind.config.ts styles the Next.js storefront in app/.
// Tailwind picks the .js one by default, so point Next at its own config.
const config = {
  plugins: {
    tailwindcss: { config: "./tailwind.config.ts" },
    autoprefixer: {},
  },
};

export default config;
