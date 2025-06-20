from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<StatsScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Estadísticas (Próximamente)'
            font_size: 24
        Button:
            text: 'Volver'
            on_press: root.manager.current = 'main'
""")

class StatsScreen(Screen):
    pass