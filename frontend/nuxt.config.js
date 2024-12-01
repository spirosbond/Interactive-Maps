// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  css: ['~/assets/styles/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
        mapboxToken: process.env.NUXT_MAPBOX_TOKEN,
        // mapboxToken: 'pk.eyJ1IjoiYmlnYXBwbGVkZXYiLCJhIjoiY200NDZtOWczMGd4ajJsc2Y1eTBsanh4MiJ9.b1wTh0FQgbrAdHmDnu5hkA',
        apiBaseUrl: process.env.NUXT_API_BASE_URL
    },
  },
})