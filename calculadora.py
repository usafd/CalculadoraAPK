from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex


# =========================
# COLORES
# =========================

FONDO = get_color_from_hex("#0B0F14")
PANEL = get_color_from_hex("#121821")
BOTON = get_color_from_hex("#252E3A")
OPERADOR = get_color_from_hex("#1677FF")
TEXTO = get_color_from_hex("#FFFFFF")
SECUNDARIO = get_color_from_hex("#AAB4C3")


# =========================
# CALCULADORA
# =========================

class Calculadora(BoxLayout):

    pantalla = StringProperty("0")
    expresion = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = dp(8)
        self.padding = dp(12)

        self.numero_actual = "0"
        self.operacion = ""
        self.numero_anterior = ""
        self.nuevo_numero = True

        # =========================
        # PANTALLA
        # =========================

        display = BoxLayout(
            orientation="vertical",
            size_hint_y=0.28,
            padding=dp(18),
            spacing=dp(5)
        )

        self.lbl_expresion = Label(
            text="",
            color=SECUNDARIO,
            font_size="20sp",
            halign="right",
            valign="middle"
        )

        self.lbl_resultado = Label(
            text="0",
            color=TEXTO,
            font_size="48sp",
            bold=True,
            halign="right",
            valign="middle"
        )

        display.add_widget(self.lbl_expresion)
        display.add_widget(self.lbl_resultado)

        self.add_widget(display)

        # =========================
        # HISTORIAL
        # =========================

        self.historial = Label(
            text="Historial\n",
            color=SECUNDARIO,
            font_size="15sp",
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.historial.bind(
            texture_size=self.historial.setter("size")
        )

        scroll = ScrollView(
            size_hint_y=0.22
        )

        scroll.add_widget(self.historial)

        self.add_widget(scroll)

        # =========================
        # BOTONES
        # =========================

        botones = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=0.5
        )

        botones_lista = [
            ("C", self.limpiar, False),
            ("+/-", self.cambiar_signo, False),
            ("%", self.porcentaje, False),
            ("÷", lambda: self.operador_pulsado("/"), True),

            ("7", lambda: self.numero_pulsado("7"), False),
            ("8", lambda: self.numero_pulsado("8"), False),
            ("9", lambda: self.numero_pulsado("9"), False),
            ("×", lambda: self.operador_pulsado("*"), True),

            ("4", lambda: self.numero_pulsado("4"), False),
            ("5", lambda: self.numero_pulsado("5"), False),
            ("6", lambda: self.numero_pulsado("6"), False),
            ("−", lambda: self.operador_pulsado("-"), True),

            ("1", lambda: self.numero_pulsado("1"), False),
            ("2", lambda: self.numero_pulsado("2"), False),
            ("3", lambda: self.numero_pulsado("3"), False),
            ("+", lambda: self.operador_pulsado("+"), True),

            ("0", lambda: self.numero_pulsado("0"), False),
            (".", lambda: self.numero_pulsado("."), False),
            ("=", self.igual, True),
        ]

        for texto, funcion, es_operador in botones_lista:

            boton = Button(
                text=texto,
                font_size="24sp",
                bold=True,
                background_normal="",
                background_color=(
                    OPERADOR if es_operador else BOTON
                ),
                color=TEXTO
            )

            boton.bind(on_press=lambda btn, f=funcion: f())

            botones.add_widget(boton)

        # Hacemos que el botón 0 ocupe dos columnas
        botones.children[-2].size_hint_x = 1

        self.add_widget(botones)

    # =========================
    # NÚMEROS
    # =========================

    def numero_pulsado(self, numero):

        if self.nuevo_numero:

            self.numero_actual = ""

            self.nuevo_numero = False

        if numero == "." and "." in self.numero_actual:
            return

        if self.numero_actual == "0" and numero != ".":
            self.numero_actual = ""

        self.numero_actual += numero

        self.actualizar_pantalla()

    # =========================
    # OPERADORES
    # =========================

    def operador_pulsado(self, operador):

        if self.operacion and not self.nuevo_numero:
            self.calcular()

        self.numero_anterior = self.numero_actual
        self.operacion = operador
        self.nuevo_numero = True

        simbolo = self.simbolo_operador(operador)

        self.expresion = f"{self.numero_anterior} {simbolo}"

        self.actualizar_pantalla()

    # =========================
    # IGUAL
    # =========================

    def igual(self):

        if not self.operacion:
            return

        segundo = self.numero_actual

        try:

            a = float(self.numero_anterior)
            b = float(segundo)

            if self.operacion == "+":
                resultado = a + b

            elif self.operacion == "-":
                resultado = a - b

            elif self.operacion == "*":
                resultado = a * b

            elif self.operacion == "/":

                if b == 0:
                    self.numero_actual = "Error"
                    self.operacion = ""
                    self.actualizar_pantalla()
                    return

                resultado = a / b

            resultado_texto = self.formatear(resultado)

            simbolo = self.simbolo_operador(self.operacion)

            operacion_completa = (
                f"{self.formatear(a)} {simbolo} "
                f"{self.formatear(b)} = "
                f"{resultado_texto}"
            )

            self.agregar_historial(operacion_completa)

            self.numero_actual = resultado_texto
            self.numero_anterior = ""
            self.operacion = ""
            self.nuevo_numero = True
            self.expresion = ""

            self.actualizar_pantalla()

        except Exception:

            self.numero_actual = "Error"
            self.actualizar_pantalla()

    # =========================
    # CÁLCULO INTERMEDIO
    # =========================

    def calcular(self):

        try:

            a = float(self.numero_anterior)
            b = float(self.numero_actual)

            if self.operacion == "+":
                resultado = a + b

            elif self.operacion == "-":
                resultado = a - b

            elif self.operacion == "*":
                resultado = a * b

            elif self.operacion == "/":

                if b == 0:
                    return

                resultado = a / b

            self.numero_actual = self.formatear(resultado)

        except:
            pass

    # =========================
    # PORCENTAJE
    # =========================

    def porcentaje(self):

        try:

            numero = float(self.numero_actual)
            numero = numero / 100

            self.numero_actual = self.formatear(numero)

            self.actualizar_pantalla()

        except:
            pass

    # =========================
    # CAMBIAR SIGNO
    # =========================

    def cambiar_signo(self):

        if self.numero_actual == "0":
            return

        try:

            numero = float(self.numero_actual)
            numero *= -1

            self.numero_actual = self.formatear(numero)

            self.actualizar_pantalla()

        except:
            pass

    # =========================
    # LIMPIAR
    # =========================

    def limpiar(self):

        self.numero_actual = "0"
        self.numero_anterior = ""
        self.operacion = ""
        self.expresion = ""
        self.nuevo_numero = True

        self.actualizar_pantalla()

    # =========================
    # HISTORIAL
    # =========================

    def agregar_historial(self, texto):

        actual = self.historial.text

        if actual == "Historial\n":
            nuevo = "Historial\n\n" + texto

        else:
            nuevo = actual + "\n" + texto

        # Limitamos el historial
        lineas = nuevo.split("\n")

        if len(lineas) > 12:
            lineas = lineas[:12]

        self.historial.text = "\n".join(lineas)

    # =========================
    # ACTUALIZAR PANTALLA
    # =========================

    def actualizar_pantalla(self):

        self.lbl_resultado.text = self.numero_actual
        self.lbl_expresion.text = self.expresion

    # =========================
    # SÍMBOLOS
    # =========================

    def simbolo_operador(self, operador):

        simbolos = {
            "+": "+",
            "-": "−",
            "*": "×",
            "/": "÷"
        }

        return simbolos.get(operador, operador)

    # =========================
    # FORMATO
    # =========================

    def formatear(self, numero):

        if float(numero).is_integer():
            return str(int(numero))

        return f"{numero:.10f}".rstrip("0").rstrip(".")


# =========================
# APP
# =========================

class CalculadoraApp(App):

    def build(self):

        self.title = "Calculadora"


        return Calculadora()


# =========================
# EJECUTAR
# =========================

if __name__ == "__main__":
    CalculadoraApp().run()