##########################################
#faktoryzacja liczb metod¹ bruteforce
#wersja sekwencyjna - do zrównoleglenia
#Bartek £awniczak 19.03.17
##########################################
import math

factorized = []

def input():
    global main_number
    main_number = int(raw_input("Enter the number: "))
    return main_number

#g³ówna funkcja faktoryzuj¹ca 
#je¿eli liczba podana w parametrze jest pierwsza, to zwraca j¹ sam¹
#je¿eli da siê podzieliæ bez reszty to zapisuje do tablicy dzielnik i zwraca podzielon¹ liczbê
def factorization(number):
    sqrted = math.sqrt(number)
    for x in range(2,int(round(sqrted+1))):
        if number%x == 0:
            number/=x
            factorized.append(x)
            return number
    factorized.append(number)
    return 1
        
input()
number = main_number
while number>2:
    result = factorization(number)
    number = result

#sprawdzenie, czy liczba jest pierwsza (wtedy tylko ona jest w tablicy 'factorized')    
if len(factorized)==1:
    print "Podana liczba jest pierwsza"
else:
    print main_number, " = ", " * ".join(str(fac) for fac in factorized)