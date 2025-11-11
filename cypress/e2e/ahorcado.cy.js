describe("Juego del Ahorcado - Flujos E2E", () => {
  // Definimos la URL de la API por separado
  const API_URL = "/api";
  const PALABRA = "python";
  const VIDAS_INICIALES = 6;

  // Antes de cada prueba visitamos la página
  beforeEach(() => {
    // 'Nueva Partida', que se hace al cargar

    cy.intercept("POST", `${API_URL}/new_game`, {
      statusCode: 200,
      body: {
        // Forzamos un estado inicial con una palabra de 6 letras
        palabra_oculta: Array(PALABRA.length).fill("_"),
        vidas: VIDAS_INICIALES,
        letras_intentadas: [],
        terminado: false,
        victoria: false,
      },
    }).as("newGame");

    // Visitamos la URL base definida en cypress.config.js
    cy.visit("/");

    // Esperamos a que la llamada de 'newGame' termine antes de continuar
    cy.wait("@newGame");
  });

  // Escenario 1: El jugador gana sin errores
  it("Scenario: El jugador adivina todas las letras sin errores (GANA)", () => {
    // Preparamos las respuestas para cada letra de "python"
    cy.intercept("POST", `${API_URL}/guess`, (req) => {
      const guess = req.body.guess;
      switch (guess) {
        case "p":
          req.reply({
            body: {
              palabra_oculta: ["p", "e", "_", "_", "_", "_"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p"],
              terminado: false,
              victoria: false,
            },
          });
          break;
        case "y":
          req.reply({
            body: {
              palabra_oculta: ["p", "y", "_", "_", "_", "_"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p", "y"],
              terminado: false,
              victoria: false,
            },
          });
          break;
        case "t":
          req.reply({
            body: {
              palabra_oculta: ["p", "y", "t", "_", "_", "_"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p", "y", "t"],
              terminado: false,
              victoria: false,
            },
          });
          break;
        case "h":
          req.reply({
            body: {
              palabra_oculta: ["p", "y", "t", "h", "_", "_"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p", "y", "t", "h"],
              terminado: false,
              victoria: false,
            },
          });
          break;
        case "o":
          req.reply({
            body: {
              palabra_oculta: ["p", "y", "t", "h", "o", "_"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p", "y", "t", "h", "o"],
              terminado: false,
              victoria: false,
            },
          });
          break;
        case "n":
          req.reply({
            body: {
              // Estado final: GANA
              palabra_oculta: ["p", "y", "t", "h", "o", "n"],
              vidas: VIDAS_INICIALES,
              letras_intentadas: ["p", "y", "t", "h", "o", "n"],
              terminado: true,
              victoria: true,
              palabra_secreta: PALABRA,
            },
          });
          break;
      }
    }).as("guessAPI");

    cy.get("#btn-p").click();
    cy.get("#word-display").should("have.text", "p _ _ _ _ _");
    cy.get("#btn-y").click();
    cy.get("#word-display").should("have.text", "p y _ _ _ _");
    cy.get("#btn-t").click();
    cy.get("#word-display").should("have.text", "p y t _ _ _");
    cy.get("#btn-h").click();
    cy.get("#word-display").should("have.text", "p y t h _ _");
    cy.get("#btn-o").click();
    cy.get("#word-display").should("have.text", "p y t h o _");
    cy.get("#btn-n").click();

    cy.get("#word-display").should("have.text", "p y t h o n");
    cy.get("#lives-left").should("have.text", VIDAS_INICIALES);
    cy.get("#game-message").should("contain", "¡Felicidades, ganaste!");
    cy.get("#btn-n").should("be.disabled"); // Verificar que el teclado se deshabilita
  });

  // Escenario 2: El jugador falla todas las letras
  it("Scenario: El jugador falla todas las letras (PIERDE)", () => {
    const letrasErroneas = ["a", "e", "i", "u", "s", "z"];
    let vidas = VIDAS_INICIALES;
    let letrasIntentadas = [];

    // Configuramos un mock dinámico para las letras erróneas
    cy.intercept("POST", `${API_URL}/guess`, (req) => {
      const guess = req.body.guess;
      if (letrasErroneas.includes(guess)) {
        vidas--; // Pierde una vida
        letrasIntentadas.push(guess);

        const esLaUltimaVida = vidas === 0;

        const responseBody = {
          palabra_oculta: ["_", "_", "_", "_", "_", "_"],
          vidas: vidas,
          letras_intentadas: [...letrasIntentadas],
          terminado: esLaUltimaVida,
          victoria: false,
        };
        if (esLaUltimaVida) {
          responseBody.palabra_secreta = PALABRA;
        }

        req.reply({ body: responseBody });
      }
    }).as("guessAPI");

    // --- Acciones del Usuario ---
    cy.get("#btn-a").click();
    cy.get("#lives-left").should("have.text", "5");
    cy.get("#btn-e").click();
    cy.get("#lives-left").should("have.text", "4");
    cy.get("#btn-i").click();
    cy.get("#lives-left").should("have.text", "3");
    cy.get("#btn-u").click();
    cy.get("#lives-left").should("have.text", "2");
    cy.get("#btn-s").click();
    cy.get("#lives-left").should("have.text", "1");
    cy.get("#btn-z").click(); // Último intento

    // --- Verificaciones Finales ---
    cy.get("#lives-left").should("have.text", "0");
    cy.get("#game-message").should(
      "contain",
      `Perdiste. La palabra era "${PALABRA}"`
    );
    cy.get("#btn-z").should("be.disabled");
  });

  // Escenario 3: El jugador gana con algunos errores
  it("Scenario: El jugador gana con algunos errores (GANA)", () => {
    // Interceptamos la secuencia: 'a' (error), luego 'p', 'y', 't', 'h', 'o', 'n' (aciertos)

    // 1. Error con 'a'
    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["_", "_", "_", "_", "_", "_"],
        vidas: 5,
        letras_intentadas: ["a"],
        terminado: false,
        victoria: false,
      },
    }).as("guessA");
    cy.get("#btn-a").click();
    cy.wait("@guessA");
    cy.get("#lives-left").should("have.text", "5");
    cy.get("#btn-a").should("be.disabled");

    // 2. Acierto con 'p'
    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "_", "_", "_", "_", "_"],
        vidas: 5,
        letras_intentadas: ["a", "p"],
        terminado: false,
        victoria: false,
      },
    }).as("guessP");
    cy.get("#btn-p").click();
    cy.wait("@guessP");
    cy.get("#word-display").should("have.text", "p _ _ _ _ _");

    // 3. Acierto con 'y'
    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "y", "_", "_", "_", "_"],
        vidas: 5,
        letras_intentadas: ["a", "p", "y"],
        terminado: false,
        victoria: false,
      },
    }).as("guessY");
    cy.get("#btn-y").click();
    cy.wait("@guessY");

    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "y", "t", "_", "_", "_"],
        vidas: 5,
        letras_intentadas: ["a", "p", "y", "t"],
        terminado: false,
        victoria: false,
      },
    }).as("guessT");
    cy.get("#btn-t").click();
    cy.wait("@guessT");

    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "y", "t", "h", "_", "_"],
        vidas: 5,
        letras_intentadas: ["a", "p", "y", "t", "h"],
        terminado: false,
        victoria: false,
      },
    }).as("guessH");
    cy.get("#btn-h").click();
    cy.wait("@guessH");

    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "y", "t", "h", "o", "_"],
        vidas: 5,
        letras_intentadas: ["a", "p", "y", "t", "h", "o"],
        terminado: false,
        victoria: false,
      },
    }).as("guessO");
    cy.get("#btn-o").click();
    cy.wait("@guessO");

    // 4. Acierto final con 'n'
    cy.intercept("POST", `${API_URL}/guess`, {
      body: {
        palabra_oculta: ["p", "y", "t", "h", "o", "n"],
        vidas: 5,
        letras_intentadas: ["a", "p", "y", "t", "h", "o", "n"],
        terminado: true,
        victoria: true,
        palabra_secreta: PALABRA,
      },
    }).as("guessN");
    cy.get("#btn-n").click();
    cy.wait("@guessN");

    // --- Verificaciones Finales ---
    cy.get("#word-display").should("have.text", "p y t h o n");
    cy.get("#lives-left").should("have.text", "5"); // Perdió una vida con la 'a'
    cy.get("#game-message").should("contain", "¡Felicidades, ganaste!");
  });

  // Escenario 4: Probar arriesgar palabra (GANA)
  it("Scenario: El jugador arriesga la palabra correcta (GANA)", () => {
    cy.intercept("POST", `${API_URL}/guess`, (req) => {
      if (req.body.guess === "python") {
        req.reply({
          body: {
            palabra_oculta: ["p", "y", "t", "h", "o", "n"],
            vidas: VIDAS_INICIALES,
            letras_intentadas: [], // No intentó letras
            terminado: true,
            victoria: true,
            palabra_secreta: PALABRA,
          },
        });
      }
    }).as("guessWord");

    cy.get("#word-input").type("python");
    cy.get("#guess-word-form").submit();
    cy.wait("@guessWord");

    cy.get("#game-message").should("contain", "¡Felicidades, ganaste!");
    cy.get("#lives-left").should("have.text", VIDAS_INICIALES);
    cy.get("#word-input").should("be.disabled"); // Formulario deshabilitado
  });

  // Escenario 5: Probar arriesgar palabra (PIERDE UNA VIDA)
  it("Scenario: El jugador arriesga la palabra incorrecta (PIERDE VIDA)", () => {
    cy.intercept("POST", `${API_URL}/guess`, (req) => {
      if (req.body.guess === "java") {
        req.reply({
          body: {
            palabra_oculta: ["_", "_", "_", "_", "_", "_"],
            vidas: 5, // Pierde una vida
            letras_intentadas: [],
            terminado: false, // El juego no termina
            victoria: false,
          },
        });
      }
    }).as("guessWord");

    cy.get("#word-input").type("java");
    cy.get("#guess-word-form").submit();
    cy.wait("@guessWord");

    cy.get("#lives-left").should("have.text", "5");
    cy.get("#game-message").should("not.contain", "Perdiste"); // Aún no pierde
    cy.get("#word-input").should("have.value", ""); // El input se limpia
  });
});
