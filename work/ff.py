#len>10 и она кратна 5 и она состоит только из чисел) возвести это число в степень равномму ее последнему элементу если она состоит только из букв вывести второй сначала и второй с конца в противном слуыае вывести в обратном пордке
text=input("введите строку")
if len(text)>10 and len(text) % 5 ==0 and text.isdigit() :
   chis=int(text)
   lastpoint=int(text[-1])
   print(chis ** lastpoint)
elif len(text)>10 and len(text) % 5 ==0 and text.isalpha() :
    sec=text[1:2]
    sec1=text[:-3:-2]
    print(sec)
    print(sec1)
else:
    newstrok=text[::-1]
    print(newstrok)
print(type(len(text)))