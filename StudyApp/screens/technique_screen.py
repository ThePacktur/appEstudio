from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""
<TechniqueScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        ScrollView:
            BoxLayout:
                id: techniques_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 10
                
        Button:
            text: 'Volver'
            size_hint_y: 0.1
            on_press: root.manager.current = 'main'
""")

class TechniqueScreen(Screen):
    def on_enter(self):
        self.load_techniques()
    
    def load_techniques(self):
        container = self.ids.techniques_container
        container.clear_widgets()
        
        app = App.get_running_app()
        for technique in app.study_manager.get_available_techniques():
            btn = Button(
                text=f"{technique.name}\n{technique.description}",
                size_hint_y=None,
                height=120,
                background_color=(0.4, 0.8, 0.6, 1) if not technique.premium else (0.8, 0.6, 0.9, 1)
            )
            btn.technique = technique
            btn.bind(on_release=self.start_technique)
            container.add_widget(btn)
        
        if not app.study_manager.subscribed:
            btn = Button(
                text="🔓 Desbloquear Técnicas Premium ($10)",
                size_hint_y=None,
                height=80,
                background_color=(0.2, 0.7, 0.3, 1)
            )
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'subscription'))
            container.add_widget(btn)
    
    def start_technique(self, instance):
        technique = instance.technique
        timer_screen = self.manager.get_screen('timer')
        timer_screen.start_technique(technique)
        self.manager.current = 'timer'