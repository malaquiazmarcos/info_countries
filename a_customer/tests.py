from django.test import TestCase


num = 2
C = 10 
cont = 0
stop = True

while stop:
    
    result = num / C
    cont += 1
    num = result

    if result >= 0 and result < 1:
        print(f'El numero tiene {cont} digitos')
        stop = False

        


