# Cómo Ejecutar el Juego

Para jugar, necesitas ejecutar tanto el servidor backend como el servidor frontend.

Abre dos terminales en la carpeta raíz de tu proyecto (agiles-2025).

### Terminal 1 (Backend):

Inicia el servidor Flask que controla la lógica del juego.

`python app.py`

Deberías ver un mensaje indicando que el servidor está corriendo en http://127.0.0.1:5000/.

### Terminal 2 (Frontend):

Sirve los archivos estáticos (HTML, CSS, JS) con un servidor simple.

## Moverse a la carpeta 'public' que creamos

`cd public`

## Iniciar un servidor HTTP simple

`python -m http.server 8000`

3. Abre tu navegador:

Ve a la dirección http://localhost:8000.

¡Listo! Tu frontend en localhost:8000 se comunicará con tu backend de Python en localhost:5000.
