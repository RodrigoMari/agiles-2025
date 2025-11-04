document.addEventListener("DOMContentLoaded", () => {
  // URL de tu API local
  const API_URL = "";
  const VIDAS_INICIALES = 6;

  // Elementos del DOM
  const wordDisplay = document.getElementById("word-display");
  const livesLeftSpan = document.getElementById("lives-left");
  const keyboardDiv = document.getElementById("keyboard");
  const gameMessage = document.getElementById("game-message");
  const resetButton = document.getElementById("reset-button");
  const guessWordForm = document.getElementById("guess-word-form");
  const wordInput = document.getElementById("word-input");
  const hangmanParts = [
    "head",
    "body",
    "left-arm",
    "right-arm",
    "left-leg",
    "right-leg",
  ];

  // INICIALIZACIÓN DEL JUEGO
  async function initializeGame() {
    try {
      // Llama a la API para crear un nuevo juego en el backend
      const response = await fetch(`${API_URL}/api/new_game`, {
        method: "POST",
        // Habilitamos 'credentials' para que las cookies de sesión funcionen
        credentials: "include",
      });
      const data = await response.json();

      // Actualizar UI con la respuesta del backend
      updateUI(data);
      resetUI();
    } catch (error) {
      console.error("Error al iniciar el juego:", error);
      gameMessage.textContent = "Error al conectar con el servidor.";
    }
  }

  // CREAR TECLADO
  function createKeyboard() {
    keyboardDiv.innerHTML = "";
    const alphabet = "abcdefghijklmnñopqrstuvwxyz";

    for (const letter of alphabet) {
      const button = document.createElement("button");
      button.textContent = letter;
      button.id = `btn-${letter}`; // ID para deshabilitarlo fácilmente
      button.classList.add(
        "letter-btn",
        "bg-gray-700",
        "hover:bg-cyan-500",
        "text-white",
        "font-bold",
        "py-2",
        "px-3",
        "rounded",
        "transition",
        "duration-200",
        "uppercase"
      );

      // Pasa la letra a handleGuess
      button.addEventListener("click", () => handleGuess(letter));

      keyboardDiv.appendChild(button);
    }
  }

  // MANEJAR INTENTO
  async function handleGuess(guess) {
    if (!guess) return; // Evitar envíos vacíos

    try {
      // Llama a la API para procesar el intento
      const response = await fetch(`${API_URL}/api/guess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ guess: guess }),
      });
      const data = await response.json();

      // Actualiza la UI con el nuevo estado del juego
      updateUI(data);
    } catch (error) {
      console.error("Error al adivinar:", error);
    }
  }

  // FUNCIÓN CENTRAL PARA ACTUALIZAR LA UI
  function updateUI(data) {
    // Actualizar palabra oculta
    wordDisplay.textContent = data.palabra_oculta.join(" ");

    // Actualizar vidas
    livesLeftSpan.textContent = data.vidas;
    updateHangmanDrawing(data.vidas);

    // Deshabilitar letras usadas
    if (data.letras_intentadas) {
      data.letras_intentadas.forEach((letter) => {
        const btn = document.getElementById(`btn-${letter}`);
        if (btn) btn.disabled = true;
      });
    }

    // Comprobar si el juego terminó
    if (data.terminado) {
      endGame(data.victoria, data.palabra_secreta);
    }
  }

  //RESET VISUAL
  function resetUI() {
    gameMessage.textContent = "";
    wordInput.value = ""; // Limpiar input de palabra
    resetButton.textContent = "Nueva Partida";

    // Resetear dibujo del ahorcado
    hangmanParts.forEach((part) =>
      document.getElementById(part).classList.add("hidden")
    );

    // Habilitar todos los botones del teclado
    document
      .querySelectorAll(".letter-btn")
      .forEach((btn) => (btn.disabled = false));
    document
      .querySelectorAll("input, button")
      .forEach((el) => (el.disabled = false));
  }

  // ACTUALIZAR DIBUJO DEL AHORCADO
  function updateHangmanDrawing(currentLives) {
    const wrongGuesses = VIDAS_INICIALES - currentLives;

    // Ocultar todas las partes primero (por si acaso)
    hangmanParts.forEach((part) =>
      document.getElementById(part).classList.add("hidden")
    );

    // Mostrar las partes correspondientes a los errores
    for (let i = 0; i < wrongGuesses; i++) {
      if (hangmanParts[i]) {
        document.getElementById(hangmanParts[i]).classList.remove("hidden");
      }
    }
  }

  // FINALIZAR JUEGO
  function endGame(isWinner, secretWord) {
    if (isWinner) {
      gameMessage.textContent = "¡Felicidades, ganaste! 🎉";
      gameMessage.classList.add("text-green-400");
      gameMessage.classList.remove("text-red-400");
    } else {
      gameMessage.textContent = `Perdiste. La palabra era "${secretWord}".`;
      gameMessage.classList.add("text-red-400");
      gameMessage.classList.remove("text-green-400");
      wordDisplay.textContent = secretWord.split("").join(" "); // Revelar
    }

    // Deshabilitar teclado y formulario
    document
      .querySelectorAll(".letter-btn")
      .forEach((btn) => (btn.disabled = true));
    document
      .querySelectorAll("input, #guess-word-form button")
      .forEach((el) => (el.disabled = true));

    resetButton.textContent = "Jugar de Nuevo";
  }

  resetButton.addEventListener("click", initializeGame);

  // Listener para el formulario de arriesgar palabra
  guessWordForm.addEventListener("submit", (e) => {
    e.preventDefault(); // Evita que la página se recargue
    const word = wordInput.value.trim().toLowerCase();
    if (word) {
      handleGuess(word);
      wordInput.value = ""; // Limpiar después de enviar
    }
  });

  // INICIO
  createKeyboard();
  initializeGame();
});
