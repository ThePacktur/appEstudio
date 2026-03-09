import json
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional


@dataclass(frozen=True)
class StudyTechnique:
    name: str
    description: str
    duration: int
    premium: bool = False


class StudyManager:
    SCHEDULE_PATTERN = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
    MAX_ROUTINE_NAME_LENGTH = 60

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
            StudyTechnique("Diagramas", "Representación visual compleja", 35, True),
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
            return

        self.subscribed = bool(data.get("subscribed", False))
        raw_routines = data.get("routines", [])
        if not isinstance(raw_routines, list):
            self.routines = []
            return

        self.routines = []
        for routine in raw_routines:
            sanitized = self._sanitize_routine(routine)
            if sanitized is not None:
                self.routines.append(sanitized)

    def save_data(self):
        data = {
            "subscribed": self.subscribed,
            "routines": self.routines,
        }

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", encoding="utf-8", dir=self.data_file.parent, delete=False) as tmp_file:
            json.dump(data, tmp_file, ensure_ascii=False, indent=2)
            tmp_name = tmp_file.name

        Path(tmp_name).replace(self.data_file)

    def get_available_techniques(self):
        return [t for t in self.techniques if not t.premium or self.subscribed]

    def validate_routine_data(self, name, technique, schedule):
        normalized_name = (name or "").strip()
        normalized_schedule = (schedule or "").strip()

        if not normalized_name:
            return False, "El nombre de la rutina es obligatorio."
        if len(normalized_name) > self.MAX_ROUTINE_NAME_LENGTH:
            return False, f"El nombre no puede superar {self.MAX_ROUTINE_NAME_LENGTH} caracteres."

        if not normalized_schedule:
            return False, "El horario es obligatorio."
        if not self.SCHEDULE_PATTERN.match(normalized_schedule):
            return False, "Horario inválido. Usa formato HH:MM (24h)."

        technique_obj = self.get_technique_by_name(technique)
        if technique_obj is None:
            return False, "La técnica seleccionada no existe."
        if technique_obj.premium and not self.subscribed:
            return False, "Esta técnica requiere suscripción premium."

        duplicated = any(
            r["name"].casefold() == normalized_name.casefold() and r["schedule"] == normalized_schedule
            for r in self.routines
        )
        if duplicated:
            return False, "Ya existe una rutina con el mismo nombre y horario."

        return True, ""

    def add_routine(self, name, technique, schedule):
        is_valid, message = self.validate_routine_data(name, technique, schedule)
        if not is_valid:
            return False, message

        routine = {
            "name": name.strip(),
            "technique": technique.strip(),
            "schedule": schedule.strip(),
            "completed": False,
        }
        self.routines.append(routine)
        self.save_data()
        return True, "Rutina guardada correctamente."

    def get_technique_by_name(self, technique_name):
        if not technique_name:
            return None
        for technique in self.techniques:
            if technique.name == technique_name:
                return technique
        return None

    def _sanitize_routine(self, routine) -> Optional[dict]:
        if not isinstance(routine, dict):
            return None

        name = str(routine.get("name", "")).strip()
        technique = str(routine.get("technique", "")).strip()
        schedule = str(routine.get("schedule", "")).strip()
        completed = bool(routine.get("completed", False))

        is_valid, _ = self.validate_routine_data(name, technique, schedule)
        if not is_valid:
            return None

        return {
            "name": name,
            "technique": technique,
            "schedule": schedule,
            "completed": completed,
        }
