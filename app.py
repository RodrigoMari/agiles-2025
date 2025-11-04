import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS

# Importamos la lógica del juego existente
from ahorca2 import Ahorcado, cargar_palabras_desde_comas

app = Flask(__name__)

# El 'static_folder' ahora apunta a tu carpeta 'public'
app = Flask(__name__, static_folder='public', static_url_path='')
app.config['SECRET_KEY'] = 'aaa' 

CORS(app, supports_credentials=True)

# Cargamos las palabras una sola vez al iniciar el servidor
try:
    PALABRAS = cargar_palabras_desde_comas("español.txt")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'español.txt'")
    PALABRAS = ["python"]

def guardar_estado_juego(juego):
    """Guarda el estado del objeto Ahorcado en la sesión."""
    session['estado_juego'] = {
        'palabra_secreta': juego.palabra_secreta,
        'vidas': juego.vidas,
        'palabra_oculta': juego.palabra_oculta,
        'letras_adivinadas': juego.letras_adivinadas,
        'palabras_intentadas': juego.palabras_intentadas,
        'letras_intentadas': juego.letras_intentadas,
        'terminado': juego.terminado,
        'victoria': juego.victoria
    }

def cargar_estado_juego():
    """Carga y reconstruye el objeto Ahorcado desde la sesión."""
    estado = session.get('estado_juego')
    if not estado:
        return None
    
    # La lista de palabras no importa
    # ya que la palabra secreta fue elegida.
    juego = Ahorcado(['dummy'], vidas=estado['vidas']) 
    
    # Sobrescribimos el estado del objeto con el guardado
    juego.palabra_secreta = estado['palabra_secreta']
    juego.palabra_oculta = estado['palabra_oculta']
    juego.letras_adivinadas = estado['letras_adivinadas']
    juego.palabras_intentadas = estado['palabras_intentadas']
    juego.letras_intentadas = estado['letras_intentadas']
    juego.terminado = estado['terminado']
    juego.victoria = estado['victoria']
    
    return juego

def obtener_estado_publico(juego):
    """Devuelve un JSON con la información que el frontend necesita."""
    estado_publico = {
        'palabra_oculta': juego.palabra_oculta,
        'vidas': juego.vidas,
        'letras_intentadas': juego.letras_intentadas,
        'terminado': juego.terminado,
        'victoria': juego.victoria
    }
    # Si el juego terminó, revela la palabra secreta
    if juego.terminado:
        estado_publico['palabra_secreta'] = juego.palabra_secreta
        
    return estado_publico


@app.route('/api/new_game', methods=['POST'])
def nuevo_juego():
    """
    Inicia una nueva partida.
    Elige una palabra aleatoria del archivo 'español.txt' cargado.
    """
    juego = Ahorcado(PALABRAS, vidas=6) 
    guardar_estado_juego(juego)
    return jsonify(obtener_estado_publico(juego))


@app.route('/api/guess', methods=['POST'])
def adivinar():
    juego = cargar_estado_juego()
    if not juego or juego.terminado:
        return jsonify({'error': 'No hay juego activo o ya terminó'}), 400

    data = request.get_json()
    intento = data.get('guess', '').lower().strip() # 'guess' puede ser una letra o una palabra

    if not intento:
        return jsonify({'error': 'No se envió ningún intento'}), 400

    # Usamos la lógica de tu clase Ahorcado
    if len(intento) == 1:
        juego.adivinar_letra(intento)
    else:
        juego.adivinar_palabra(intento)
    
    guardar_estado_juego(juego)
    return jsonify(obtener_estado_publico(juego))

# --- INICIO: NUEVAS RUTAS PARA SERVIR EL FRONTEND ---

@app.route('/')
def serve_index():
    """Sirve el archivo index.html en la ruta raíz."""
    # Busca 'index.html' dentro de la 'static_folder' (que definimos como 'public')
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Sirve cualquier otro archivo estático (como css/style.css o js/script.js)
    que se pida desde la carpeta 'public'.
    """
    # Esto es necesario para que index.html pueda cargar css/style.css y js/script.js
    return send_from_directory(app.static_folder, filename)

# --- FIN: NUEVAS RUTAS PARA SERVIR EL FRONTEND ---

##if __name__ == '__main__':
    app.run(debug=True, port=5000)