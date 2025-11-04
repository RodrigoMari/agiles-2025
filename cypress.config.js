const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    // URL donde se sirve tu frontend (el servidor 'python -m http.server 8000')
    baseUrl: "http://localhost:8000",

    // Esto le dice a Cypress que no necesitamos el archivo cypress/support/e2e.js
    supportFile: false,

    // No necesitamos esto para pruebas locales, pero es buena práctica
    video: false,
    screenshotOnRunFailure: false,
  },
});
