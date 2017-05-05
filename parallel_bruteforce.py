##########################################
# faktoryzacja liczb metoda bruteforce
# wersja rownolegla wykorzystujaca rdd
# Bartek Lawniczak 10.04.17
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
    rdd = sc.parallelize(range(2,long(round(sqrted + 1))),partitions)
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
