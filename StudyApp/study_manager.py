import json
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class StudyTechnique:
    name: str
    description: str
    duration: int
    premium: bool = False

class StudyManager:
    def __init__(self):
        self.data_file = Path(__file__).resolve().parent / "user_data.json"
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
        if not self.data_file.exists():
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Si el archivo está corrupto o inaccesible, continuamos con estado por defecto.
            return

        self.subscribed = bool(data.get("subscribed", False))
        self.routines = [
            routine for routine in data.get("routines", [])
            if all(key in routine for key in ("name", "technique", "schedule"))
        ]
    
    def save_data(self):
        data = {
            'subscribed': self.subscribed,
            'routines': self.routines
        }
        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_available_techniques(self):
        return [t for t in self.techniques if not t.premium or self.subscribed]
    
    def add_routine(self, name, technique, schedule):
        name = name.strip()
        schedule = schedule.strip()

        self.routines.append({
            'name': name,
            'technique': technique,
            'schedule': schedule,
            'completed': False
        })
        self.save_data()
