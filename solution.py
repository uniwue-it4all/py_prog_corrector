def avgAlterPatienten(krankenhaus) -> float:
    gesamt_alter: int = 0
    anzahl_patienten: int = 0

    for station in krankenhaus.stationen:
        for patient in station.patienten:
            gesamt_alter += patient.alter
        anzahl_patienten += len(station.patienten)

    if anzahl_patienten == 0:
        return -1
    else:
        return gesamt_alter / anzahl_patienten
