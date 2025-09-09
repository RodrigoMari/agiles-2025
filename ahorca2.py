class Ahorcado:
    def __init__(self, palabras, vidas=5):
        self.palabra_secreta = random.choice(palabras)
        self.vidas = vidas
        self.palabra_oculta = ['_'] * len(self.palabra_secreta)
        self.letras_adivinadas = []  # Letras acertadas
        self.letras_intentadas = []  # Todas las letras intentadas (acertadas y no acertadas, sin repetir)
        self.terminado = False
        self.victoria = False