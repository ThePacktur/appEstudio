from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""
<TimerScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: root.technique_name
            font_size: 30
            bold: True
            size_hint_y: 0.2
            
        Label:
            text: root.format_time()
            font_size: 48
            size_hint_y: 0.4
            
        ProgressBar:
            value: root.time_left
            max: root.initial_time
            size_hint_y: 0.1
        
        BoxLayout:
            size_hint_y: 0.3
            spacing: 20
            
            Button:
                text: 'Iniciar' if not root.is_running else 'Pausar'
                on_press: root.start_timer() if not root.is_running else root.pause_timer()
                background_color: 0, 0.7, 0, 1
                
            Button:
                text: 'Reiniciar'
                on_press: root.reset_timer()
                background_color: 0.8, 0.5, 0, 1
                
            Button:
                text: 'Volver'
                on_press: root.manager.current = 'techniques'
                background_color: 0.8, 0, 0, 1
""")

class TimerScreen(Screen):
    time_left = NumericProperty(0)
    initial_time = NumericProperty(1)
    technique_name = StringProperty("")
    is_running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.technique = None
        self.event = None

    def start_technique(self, technique):
        self.technique = technique
        self.time_left = technique.duration * 60
        self.initial_time = self.time_left
        self.technique_name = technique.name
        self.is_running = False
    
    def start_timer(self):
        if not self.is_running and self.time_left > 0:
            self.is_running = True
            self.event = Clock.schedule_interval(self.update_timer, 1)
    
    def pause_timer(self):
        if self.is_running and self.event is not None:
            self.is_running = False
            self.event.cancel()
            self.event = None
    
    def reset_timer(self):
        if self.technique is None:
            return

        self.time_left = self.technique.duration * 60
        self.initial_time = self.time_left
        if self.event is not None:
            self.event.cancel()
            self.event = None
        self.is_running = False
    
    def update_timer(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            if self.event is not None:
                self.event.cancel()
                self.event = None
            self.time_left = 0
            self.is_running = False
            self.show_completion_popup()
    
    def show_completion_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="¡Sesión completada!"))
        btn = Button(text="Cerrar", size_hint_y=0.4)
        popup = Popup(title="Felicitaciones", content=content, size_hint=(0.7, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()
    
    def format_time(self):
        minutes, seconds = divmod(self.time_left, 60)
        return f"{minutes:02d}:{seconds:02d}"