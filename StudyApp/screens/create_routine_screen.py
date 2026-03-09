from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

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
        self.technique_dropdown = None

    def create_dropdown(self):
        if self.technique_dropdown:
            return

        self.technique_dropdown = DropDown()
        app = App.get_running_app()
        for technique in app.study_manager.get_available_techniques():
            btn = Button(text=technique.name, size_hint_y=None, height=44)
            btn.technique = technique
            btn.bind(on_release=lambda btn: self.select_technique(btn.technique))
            self.technique_dropdown.add_widget(btn)

    def open_technique_dropdown(self):
        self.create_dropdown()
        self.technique_dropdown.open(self.ids.technique_btn)

    def select_technique(self, technique):
        self.technique = technique
        self.ids.technique_btn.text = technique.name
        self.technique_dropdown.dismiss()

    def save_routine(self):
        name = self.ids.routine_name.text
        schedule = self.ids.schedule.text

        if not self.technique:
            self._show_message("Validación", "Selecciona una técnica para continuar.")
            return

        app = App.get_running_app()
        success, message = app.study_manager.add_routine(name, self.technique.name, schedule)

        if not success:
            self._show_message("Error de validación", message)
            return

        self._show_message("Éxito", message)
        self.manager.current = 'routines'

    def _show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='Aceptar', size_hint_y=0.4)
        popup = Popup(title=title, content=content, size_hint=(0.75, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()
