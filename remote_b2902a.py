import sys
from pyvisa import ResourceManager
from time import sleep, time
# rm = ResourceManager()
# print(rm.list_resources())
# b2902a_1 = rm.list_resources()[0]
# inst = rm.open_resource(b2902a_1)
# print(inst.query("*IDN?"))

# Spot measurement
# inst.write("*RST")
# inst.write("*CLS")
# inst.write(":sour1:func:mode volt")
# inst.write(":sour2:func:mode curr")
# inst.write(":sens1:curr:rang:auto on")
# inst.write(":sens2.volt:rang:auto on")
# inst.write("outp1 on")
# inst.write("outp2 on")
# inst.write(":sour1:volt 20")





# Stairs_measurement
# npoint = 20
# inst.write("*RST")
# inst.write(":sour:func:mode volt")   
# inst.write(":sour:volt:mode swe")
# inst.write(":sour:volt:start 0")
# inst.write(":sour:volt:stop 1")
# inst.write(":sour:volt:poin {}".format(npoint))
# inst.write(":sens:func \"curr\"")
# inst.write(":sens:curr:nplc 1")
# inst.write(":sens:curr:prot 0.1")
# inst.write(":trig:sour aint")
# inst.write(":trig:coun {}".format(npoint))
# inst.write(":outp on")
# ans = inst.query(":fetc:arr:curr? (@1)").strip().split(",")

# while (True):
#     if int(inst.query(":STAT:OPER:COND?")) & 18 == 18:
#         break

# Задание постоянного напряжения
def const_voltage_ch1(voltage, current, count, file_name):
    rm = ResourceManager()
    print(rm.list_resources())
    b2902a_1 = rm.list_resources()[0]
    inst = rm.open_resource(b2902a_1)

    # Spot measurement

    inst.write("*RST")
    inst.write("*CLS")
    inst.write(":sour1:func:mode volt")
    # inst.write(":sour2:func:mode curr")
    inst.write(f":sens1:curr:rang:auto off") 
    inst.write(f":sens1:curr:rang:lim {current}") # не задается предел по току
    # inst.write(":sens2.volt:rang:auto on")
    inst.write("outp1 on")
    # inst.write("outp2 on")
    inst.write(f":sour1:volt {voltage}")
    log_file = open(f"{file_name}", "w", encoding="utf-8")
    log_file.write("Время Напряжение\t Ток\n")
    a = time()

    print("Напряжение" + "\t" + "Ток")
    for i in range(1, int(count)):
        obj = {"Время": time() - a,
        "Напряжение":inst.query("meas:volt? (@1)").strip(),
        "Ток":inst.query("meas:curr? (@1)").strip()}
        print(obj["Напряжение"] + "\t" +
            obj["Ток"])
        
        log_file.write(f'{obj["Время"]:.4}, {obj["Напряжение"]}, {obj["Ток"]} \n')
        sleep(1.00) # задержка между измерениями


    inst.write("outp1 off")
    # inst.write("outp2 off")
    log_file.close()
    # print(voltage)
    # print(current)


if __name__ == "__main__":
    arg = sys.argv[1:] # срезом убираем название скрипта
    # print(arg)
    const_voltage_ch1(*arg) # распаковываем все аргументы в функцию