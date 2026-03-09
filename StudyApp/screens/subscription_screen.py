from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<SubscriptionScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: 'Suscripción Premium'
            font_size: 30
            bold: True
            size_hint_y: 0.2
            
        Label:
            text: 'Desbloquea todas las técnicas de estudio por solo $10'
            font_size: 18
            size_hint_y: 0.3
            
        Button:
            text: 'Suscribirse ($10)'
            size_hint_y: 0.2
            background_color: 0.2, 0.7, 0.3, 1
            on_press: root.subscribe()
            
        Button:
            text: 'Volver'
            size_hint_y: 0.1
            on_press: root.manager.current = 'main'
""")

class SubscriptionScreen(Screen):
    def subscribe(self):
        app = App.get_running_app()

        if app.study_manager.subscribed:
            self._show_popup("Información", "Ya tienes una suscripción activa.")
            return

        app.study_manager.subscribed = True
        app.study_manager.save_data()

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="¡Suscripción exitosa!\nAhora tienes acceso completo"))
        btn = Button(text="Aceptar", size_hint_y=0.4)
        popup = Popup(title="Felicitaciones", content=content, size_hint=(0.7, 0.4))
        btn.bind(on_release=lambda x: self.post_subscription(popup))
        content.add_widget(btn)
        popup.open()
    
    def post_subscription(self, popup):
        popup.dismiss()
        self.manager.current = 'techniques'

    def _show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text="Aceptar", size_hint_y=0.4)
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()