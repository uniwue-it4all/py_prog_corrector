from typing import List


class Medikament:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Rezept:
    def __init__(self, id: int, medikamente: List[Medikament]):
        self.id = id
        self.medikamente = medikamente


class Person:
    def __init__(self, id: str, name: str, alter: int):
        self.id = id
        self.name = name
        self.alter = alter


class Patient(Person):
    def __init__(self, id: str, name: str, alter: int, rezepte: List[Rezept]):
        super().__init__(id, name, alter)
        self.rezepte = rezepte


class Krankenschwester(Person):
    def __init__(self, id: str, name: str, alter: int):
        super().__init__(id, name, alter)


class Doktor(Person):
    def __init__(self, id: str, name: str, alter: int, patienten: List[Patient], rezepte: List[Rezept]):
        super().__init__(id, name, alter)
        self.patienten = patienten
        self.rezepte = rezepte


class Station:
    def __init__(self, nummer: int, doktoren: List[Doktor], krankenschwestern: List[Krankenschwester],
                 patienten: List[Patient]):
        self.nummer = nummer
        self.doktoren = doktoren
        self.krankenschwestern = krankenschwestern
        self.patienten = patienten


class Krankenhaus:
    def __init__(self, stationen: List[Station]):
        self.stationen = stationen

    def durchschnitt_alter_patienten(self):
        # {1}
        gesamt_alter: int = 0
        anzahl_patienten: int = 0

        print(len(self.stationen))

        for station in self.stationen:
            for patient in station.patienten:
                gesamt_alter += patient.alter
            anzahl_patienten += len(station.patienten)

        if anzahl_patienten == 0:
            return -1
        else:
            return gesamt_alter / anzahl_patienten

