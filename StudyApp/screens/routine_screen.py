
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""
<RoutineScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        ScrollView:
            BoxLayout:
                id: routines_container
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

class RoutineScreen(Screen):
    def on_enter(self):
        self.load_routines()
    
    def load_routines(self):
        container = self.ids.routines_container
        container.clear_widgets()
        
        app = App.get_running_app()
        if not app.study_manager.routines:
            container.add_widget(Button(
                text="Aún no tienes rutinas. Crea tu primera rutina.",
                size_hint_y=None,
                height=80,
                background_color=(0.7, 0.7, 0.7, 1),
                disabled=True,
            ))

        for routine in app.study_manager.routines:
            btn = Button(
                text=(
                    f"{routine.get('name', 'Sin nombre')}\n"
                    f"Técnica: {routine.get('technique', 'N/A')} - "
                    f"Horario: {routine.get('schedule', 'N/A')}"
                ),
                size_hint_y=None,
                height=100,
                background_color=(0.5, 0.7, 0.9, 1)
            )
            container.add_widget(btn)

        btn = Button(
            text="+ Crear Nueva Rutina",
            size_hint_y=None,
            height=80,
            background_color=(0.3, 0.5, 0.8, 1)
        )
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'create_routine'))
        container.add_widget(btn)