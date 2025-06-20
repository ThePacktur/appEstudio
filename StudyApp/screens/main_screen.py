from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Button:
            text: 'Técnicas de Estudio'
            on_press: root.manager.current = 'techniques'
            size_hint_y: 0.2
            background_color: 0.2, 0.6, 0.9, 1
            
        Button:
            text: 'Mis Rutinas'
            on_press: root.manager.current = 'routines'
            size_hint_y: 0.2
            background_color: 0.3, 0.7, 0.5, 1
            
        Button:
            text: 'Estadísticas'
            on_press: root.manager.current = 'stats'
            size_hint_y: 0.2
            background_color: 0.8, 0.5, 0.2, 1
            
        Button:
            text: 'Suscripción'
            on_press: root.manager.current = 'subscription'
            size_hint_y: 0.2
            background_color: 0.9, 0.6, 0.2, 1
""")

class MainScreen(Screen):
    pass