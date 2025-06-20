import json
import os

class StudyTechnique:
    def __init__(self, name, description, duration, premium=False):
        self.name = name
        self.description = description
        self.duration = duration
        self.premium = premium

class StudyManager:
    def __init__(self):
        self.techniques = [
            StudyTechnique("Pomodoro", "25 min estudio + 5 min descanso", 25),
            StudyTechnique("Feynman", "Explica conceptos en términos simples", 30),
            StudyTechnique("Mapa Mental", "Organiza ideas visualmente", 20),
            StudyTechnique("Repetición Espaciada", "Revisión en intervalos crecientes", 15),
            StudyTechnique("SQ3R", "Explorar, Preguntar, Leer, Recitar, Repasar", 45),
            StudyTechnique("Active Recall", "Recuperación activa de información", 25, True),
            StudyTechnique("Interleaving", "Alternar entre temas diferentes", 40, True),
            StudyTechnique("Autoevaluación", "Pruebas periódicas de conocimiento", 30, True),
            StudyTechnique("Analogías", "Relacionar conceptos con experiencias", 20, True),
            StudyTechnique("Diagramas", "Representación visual compleja", 35, True)
        ]
        
        self.routines = []
        self.subscribed = False
        self.load_data()
    
    def load_data(self):
        if os.path.exists("user_data.json"):
            with open("user_data.json", 'r') as f:
                data = json.load(f)
                self.subscribed = data.get('subscribed', False)
                self.routines = data.get('routines', [])
    
    def save_data(self):
        data = {
            'subscribed': self.subscribed,
            'routines': self.routines
        }
        with open("user_data.json", 'w') as f:
            json.dump(data, f)
    
    def get_available_techniques(self):
        return [t for t in self.techniques if not t.premium or self.subscribed]
    
    def add_routine(self, name, technique, schedule):
        self.routines.append({
            'name': name,
            'technique': technique,
            'schedule': schedule,
            'completed': False
        })
        self.save_data()