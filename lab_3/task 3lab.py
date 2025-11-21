#класс баскетболисты гед при сосздании обьекта имя возраст игровая позиция рост кол очков статус играет невзаявки пользователь может добавить удалить игрока менять статус ,возрост очки
class PlayerError(Exception):
    pass

class ErrorHigh(PlayerError):
    pass

class ErrorAge(PlayerError):
    pass

class PlayerNotFound(PlayerError):
    pass
class ErrorPoints(PlayerError):
    pass


class bas_player:
    def __init__(self, name: str, age: int, position: str,
                 high: float, points: int, status: str):

        if age < 0:
            raise ErrorAge("Возраст не может быть отрицательным!")
        if high < 0.0:
            raise ErrorHigh("Неверный рост!")

        self.name = name
        self.age = age
        self.position = position
        self.high = high
        self.points = points
        self.status = status

    def __str__(self):
        return (f"Игрок c именем: {self.name}, возраст: {self.age}, позиция: {self.position}, "
                f"рост: {self.high}, очки: {self.points}, статус: {self.status}")


class bas_team:
    def __init__(self):
        self.players = []

    def add_player(self, player: bas_player):
        self.players.append(player)

    def remove_player(self, name):
        for i, player in enumerate(self.players):
            if player.name == name:
                del self.players[i]
                return
        raise PlayerNotFound("Такой игрок не найден!")

    def spisok_player(self):
        if not self.players:
            print("Список игроков пуст")
            return
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player}")

    def save_spis(self):
        with open("spisok.txt", "w", encoding="utf-8") as f:
            for player in self.players:
                f.write(str(player) + "\n")

    def find(self, name):
        for player in self.players:
            if player.name == name:
                return player
        raise PlayerNotFound("Игрок не найден!")

    def change_status(self, name, new_status):
        player = self.find(name)
        player.status = new_status

    def change_age(self, name, new_age):
        if new_age < 0:
            raise ErrorAge("Возраст неверный")
        player = self.find(name)
        player.age = new_age

    def change_points(self, name, new_points):
        if new_points < 0:
            raise ErrorPoints("Ты силен но меньше 0 не получится")
        player = self.find(name)
        player.points = new_points



def main():
    bas = bas_team()
    while True:
        print("""
    1. Добавить игрока
    2. Удалить игрока
    3. Показать игроков
    4. Изменить очки
    5. Изменить статус
    6. Изменить возраст
    7. Сохранение в файл
    0. Выход
    """)

        choice = input("Ваш выбор: ")
        try:
            if choice == "1":
                name = input("Имя: ")
                age = int(input("Возраст: "))
                position = input("Позиция: ")
                high = float(input("Рост: "))
                points = int(input("Очки в последнем матче: "))
                status = input("Статус (играет/вне заявки): ")

                bas.add_player(bas_player(
                    name, age, position, high, points, status
                ))

            elif choice == "2":
                bas.remove_player(input("Имя игрока: "))

            elif choice == "3":
                bas.spisok_player()

            elif choice == "4":
                name = input("Имя: ")
                points = int(input("Новые очки: "))
                bas.change_points(name, points)


            elif choice == "5":
                name=input("Имя: ")
                status=input("Новый статус: ")
                bas.change_status(name,status)

            elif choice == "6":
                name=input("Имя: ")
                age=int(input("Новый возраст: "))
                bas.change_age(name,age)

            elif choice == "7":
                bas.save_spis()
                print("Cохранено")

            elif choice == "0":
                break

            else:
                print("Неизвестный пункт меню!")

        except Exception as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()



