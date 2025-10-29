password = input("Введите пароль: ")
if len(password) < 16:
    print("Слишком короткий")
elif password.isalpha() or password.isdigit():

    print("Слабый пароль")
else:
    print("Надежный пароль")
#Decimal Digit Number -есть такие символы в таблице unicode метод isdigit сверяя каждый элемент нашего пороля по таблице как символы '0' <= ch <= '9'(примерно так) на таком же принципе воркает альфа