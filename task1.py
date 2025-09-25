surname, name, patronymic = input("Введите фамилию, имя и отчество: ").split() #Ввод через 1 пробел
surname = surname.capitalize()      #делаем 1 заглавную букву а остальное маленькое  если ввели некультурно
name = name.capitalize()          #делаем 1 заглавную букву а остальное маленькое  если ввели некультурно
patronymic = patronymic.capitalize()#делаем 1 заглавную букву а остальное маленькое  если ввели некультурно
print(f"{surname} {name[0]}.{patronymic[0]}.")