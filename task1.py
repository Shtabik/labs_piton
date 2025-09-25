surname, name, patronymic = input("Введите фамилию, имя и отчество:(все через пробел) ").split() #Ввод через 1 пробел
print(f"{surname} {name[0]}.{patronymic[0]}.")