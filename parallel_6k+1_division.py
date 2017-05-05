##########################################
# faktoryzacja liczb metoda 6k+1
# wersja rownolegla wykorzystujaca rdd
# powinno byæ szybsze od bruteforce
# Bartek Lawniczak 05.05.17
#bez errorow wykonuje dzielenie 16-cyforwej liczby (okolo2^40)
##########################################
import math
from pyspark import SparkContext

sc = SparkContext(appName="mypi")
partitions = 2                                      #number from lecture
main_number = long(raw_input("Enter the number: "))  #raw_input - need to be replaced in the future
factorized = []
x = number = main_number

while x>1:
    sqrted = math.sqrt(number)
    divisors = [2,3]
    x = 1
    while 6*x+1 < round(sqrted):
        divisors.append(6*x+1)
        x = x+1
    rdd = sc.parallelize(range(2,divisors,partitions)
    try:
        x = rdd.filter(lambda x: (number%x==0)).first()
    except ValueError:
        x = 1

    if x>1:
        number /= x
        factorized.append(x)
    else:
        factorized.append(number)

if len(factorized) == 1:
    print "Podana liczba jest pierwsza"
else:
    print main_number, " = ", " * ".join(str(fac) for fac in factorized)

sc.stop()
