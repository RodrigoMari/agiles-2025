import random

def inicializar_juego(palabras):
    """Elige una palabra al azar y crea la palabra oculta."""
    palabra = random.choice(palabras)
    palabra_oculta = ['_'] * len(palabra)
    return palabra, palabra_oculta

def actualizar_palabra_oculta(palabra_secreta, palabra_oculta, letra):
    """Actualiza la palabra oculta con la letra si está en la palabra secreta."""
    for i in range(len(palabra_secreta)):
        if palabra_secreta[i] == letra:
            palabra_oculta[i] = letra
    return palabra_oculta

def letra_en_palabra(letra, palabra):
    """Retorna True si la letra está en la palabra."""
    return letra in palabra

def solo_letras(letra):
    return len(letra) == 1 and letra.isalpha()

def juego_ahorcado():
    palabras = ['python', 'ahorcado', 'juego', 'programacion', 'desarrollo']
    palabra_secreta, palabra_oculta = inicializar_juego(palabras)
    letras_adivinadas = []
    intentos_restantes = 6

    print("¡Bienvenido al juego del Ahorcado!")

    while intentos_restantes > 0 and '_' in palabra_oculta:
        print("\nPalabra: ", ' '.join(palabra_oculta))
        print("Letras adivinadas:", ', '.join(letras_adivinadas))
        print("Intentos restantes:", intentos_restantes)
        
        letra = input("Adivina una letra: ").lower()

        if solo_letras() == True:
            print("Por favor, ingresa solo una letra.")
            continue

        if letra in letras_adivinadas:
            print("Ya adivinaste esa letra.")
            continue

        letras_adivinadas.append(letra)

        if letra_en_palabra(letra, palabra_secreta):
            palabra_oculta = actualizar_palabra_oculta(palabra_secreta, palabra_oculta, letra)
            print("¡Bien! La letra está en la palabra.")
        else:
            intentos_restantes -= 1
            print("Incorrecto. Esa letra no está en la palabra.")

    if '_' not in palabra_oculta:
        print("\n¡Felicidades! Adivinaste la palabra:", palabra_secreta)
    else:
        print("\n¡Perdiste! La palabra era:", palabra_secreta)

# Corrección aquí:
if __name__ == '__main__':
    juego_ahorcado()
