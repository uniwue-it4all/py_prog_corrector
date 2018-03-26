def average(my_list):
    length = len(my_list)
    if length == 0:
        return "Fehler"
    else:
        return sum(my_list) / length
