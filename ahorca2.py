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
        else:
            self.descuenta_vida()