from classes import Patient, Station, Krankenhaus


def convert_input(input):
    stationen = []

    # Instantiate all stations
    for (stations_index, alter_liste_station) in enumerate(input):
        patienten_station = []

        # Instantiate all patients on station
        for (patient_index, patient_alter) in enumerate(alter_liste_station):
            patient_id = "{}_{}".format(stations_index, patient_index)
            patienten_station.append(Patient(id=patient_id, name='', alter=patient_alter, rezepte=[]))

        stationen.append(Station(stations_index, doktoren=[], krankenschwestern=[], patienten=patienten_station))

    # Instantiate hospital
    return Krankenhaus(stationen)
