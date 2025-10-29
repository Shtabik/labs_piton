# Тарифные параметры
prise = 24.99
inminutes = 60
insms = 30
inmb = 1024
#переизбыток
extraminute = 0.89
extrasms = 0.59
extramb = 0.79
tax_rate = 0.02           # 2%

# Ввод данных
minutes = int(input("Количество использованных минут: "))
sms = int(input("Количество смс: "))
mb = int(input("Объем интернет-трафика (МБ): "))

# Вычисляем дополнительные услуги
dopminutes = max(0, minutes - inminutes)
dopsms = max(0, sms - insms)
dopmb = max(0, mb - inmb)

dopminutes_cost = dopminutes * extraminute
dopsms_cost = dopsms * extrasms
dopmb_cost = dopmb * extramb

# Базовая сумма + доплаты
subtotal = prise + dopminutes_cost + dopsms_cost + dopmb_cost

# Налог
tax_amount = subtotal * tax_rate

# Итоговая сумма
total = subtotal + tax_amount

# Вывод
print(f"Базовая стоимость: {prise:.2f} руб.")
if dopminutes > 0:
    print(f"Дополнительно за минуты: {dopminutes_cost:.2f} руб.")
if dopsms > 0:
    print(f"Дополнительно за смс: {dopsms_cost:.2f} руб.")
if dopmb > 0:
    print(f"Дополнительно за интернет: {dopmb_cost:.2f} руб.")
print(f"Дополнительно за все использование функций:{dopminutes_cost+dopsms_cost+dopmb_cost}")
print(f"Налог (2%): {tax_amount:.2f} руб.")
print(f"Итого к оплате: {total:.2f} руб.")
