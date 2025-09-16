import random

class Ahorcado:
    def __init__(self, palabras, vidas=5):
        self.palabra_secreta = random.choice(palabras)
        self.vidas = vidas
        self.palabra_oculta = ['_'] * len(self.palabra_secreta)
        self.letras_adivinadas = []  # Letras acertadas
        self.letras_intentadas = []  # Todas las letras intentadas (acertadas y no acertadas, sin repetir)
        self.terminado = False
        self.victoria = False

    def descuenta_vida(self):
        self.vidas -= 1

    def adivinar_letra(self, letra):
        if self.terminado or letra in self.letras_intentadas:
            return
        self.letras_intentadas.append(letra)
        if letra in self.palabra_secreta:
            self.letras_adivinadas.append(letra)
            for i, l in enumerate(self.palabra_secreta):
                if l == letra:
                    self.palabra_oculta[i] = letra
        else:
            self.descuenta_vida()

    def adivinar_palabra(self, palabra):
        if self.terminado or len(palabra) < 2: 
            return  # Si el juego ha terminado, o la palabra es de longitud 1 (en realidad es una letra)
        if palabra == self.palabra_secreta:
            self.palabra_oculta = list(self.palabra_secreta)
            self.victoria = True
            self.terminado = True

