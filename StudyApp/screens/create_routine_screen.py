from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""
<CreateRoutineScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        TextInput:
            id: routine_name
            hint_text: 'Nombre de la rutina'
            size_hint_y: 0.1
            
        Button:
            id: technique_btn
            text: 'Seleccionar técnica'
            size_hint_y: 0.1
            on_release: root.open_technique_dropdown()
            
        TextInput:
            id: schedule
            hint_text: 'Horario (HH:MM)'
            size_hint_y: 0.1
            
        Button:
            text: 'Guardar Rutina'
            size_hint_y: 0.1
            background_color: 0, 0.7, 0, 1
            on_press: root.save_routine()
            
        Button:
            text: 'Volver'
            size_hint_y: 0.1
            on_press: root.manager.current = 'routines'
""")

class CreateRoutineScreen(Screen):
    def on_enter(self):
        self.ids.routine_name.text = ""
        self.ids.schedule.text = ""
        self.ids.technique_btn.text = "Seleccionar técnica"
        self.technique = None
        self.technique_dropdown = None  # Inicializar como None
    
    def create_dropdown(self):
        if not self.technique_dropdown:
            self.technique_dropdown = DropDown()
            app = App.get_running_app()
            for technique in app.study_manager.get_available_techniques():
                btn = Button(
                    text=technique.name,
                    size_hint_y=None,
                    height=44
                )
                btn.technique = technique
                btn.bind(on_release=lambda btn: self.select_technique(btn.technique))
                self.technique_dropdown.add_widget(btn)
    
    def open_technique_dropdown(self):  # Nuevo método
        self.create_dropdown()
        self.technique_dropdown.open(self.ids.technique_btn)
    
    def select_technique(self, technique):
        self.technique = technique
        self.ids.technique_btn.text = technique.name
        self.technique_dropdown.dismiss()
    
    def save_routine(self):
        name = self.ids.routine_name.text
        schedule = self.ids.schedule.text
        
        if not name or not schedule or not self.technique:
            return
        
        app = App.get_running_app()
        app.study_manager.add_routine(name, self.technique.name, schedule)
        self.manager.current = 'routines'