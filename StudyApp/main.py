from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from study_manager import StudyManager
from screens.main_screen import MainScreen
from screens.technique_screen import TechniqueScreen
from screens.timer_screen import TimerScreen
from screens.routine_screen import RoutineScreen
from screens.create_routine_screen import CreateRoutineScreen
from screens.subscription_screen import SubscriptionScreen
from screens.stats_screen import StatsScreen

class StudyApp(App):
    def build(self):
        self.study_manager = StudyManager()
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(TechniqueScreen(name='techniques'))
        sm.add_widget(TimerScreen(name='timer'))
        sm.add_widget(RoutineScreen(name='routines'))
        sm.add_widget(CreateRoutineScreen(name='create_routine'))
        sm.add_widget(SubscriptionScreen(name='subscription'))
        sm.add_widget(StatsScreen(name='stats'))
        
        return sm

if __name__ == '__main__':
    StudyApp().run()