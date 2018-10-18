# MANSEDS Rocketry 2nd Stage Altitude Recording
# Authors: Ethan Ramsay, Ben Shortland, Oscar Driver

import time
import smbus
import math

### Read corrected temperature and pressure
# Get I2C bus
bus = smbus.SMBus(1)

def ReadTempAndPressure():
    # BMP280 address, 0x76(118)
    # Read data back from 0x88(136), 24 bytes
    b1 = bus.read_i2c_block_data(0x76, 0x88, 24)

    # Convert the data
    # Temp coefficents
    dig_T1 = b1[1] * 256 + b1[0]
    dig_T2 = b1[3] * 256 + b1[2]
    if dig_T2 > 32767 :
        dig_T2 -= 65536
    dig_T3 = b1[5] * 256 + b1[4]
    if dig_T3 > 32767 :
        dig_T3 -= 65536

    # Pressure coefficents
    dig_P1 = b1[7] * 256 + b1[6]
    dig_P2 = b1[9] * 256 + b1[8]
    if dig_P2 > 32767 :
        dig_P2 -= 65536
    dig_P3 = b1[11] * 256 + b1[10]
    if dig_P3 > 32767 :
        dig_P3 -= 65536
    dig_P4 = b1[13] * 256 + b1[12]
    if dig_P4 > 32767 :
        dig_P4 -= 65536
    dig_P5 = b1[15] * 256 + b1[14]
    if dig_P5 > 32767 :
        dig_P5 -= 65536
    dig_P6 = b1[17] * 256 + b1[16]
    if dig_P6 > 32767 :
        dig_P6 -= 65536
    dig_P7 = b1[19] * 256 + b1[18]
    if dig_P7 > 32767 :
        dig_P7 -= 65536
    dig_P8 = b1[21] * 256 + b1[20]
    if dig_P8 > 32767 :
        dig_P8 -= 65536
    dig_P9 = b1[23] * 256 + b1[22]
    if dig_P9 > 32767 :
        dig_P9 -= 65536

    # BMP280 address, 0x76(118)
    # Select Control measurement register, 0xF4(244)
    #		0x27(39)	Pressure and Temperature Oversampling rate = 1
    #					Normal mode
    bus.write_byte_data(0x76, 0xF4, 0x27)
    # BMP280 address, 0x76(118)
    # Select Configuration register, 0xF5(245)
    #		0xA0(00)	Stand_by time = 1000 ms
    bus.write_byte_data(0x76, 0xF5, 0xA0)

    time.sleep(0.5)

    # BMP280 address, 0x76(118)
    # Read data back from 0xF7(247), 8 bytes
    # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
    # Temperature xLSB, Humidity MSB, Humidity LSB
    data = bus.read_i2c_block_data(0x76, 0xF7, 8)

    # Convert pressure and temperature data to 19-bits
    adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
    adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16

    # Temperature offset calculations
    var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
    var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
    t_fine = (var1 + var2)
    cTemp = (var1 + var2) / 5120.0

    # Pressure offset calculations
    var1 = (t_fine / 2.0) - 64000.0
    var2 = var1 * var1 * (dig_P6) / 32768.0
    var2 = var2 + var1 * (dig_P5) * 2.0
    var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
    var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * (dig_P1)
    p = 1048576.0 - adc_p
    p = (p - (var2 / 4096.0)) * 6250.0 / var1
    var1 = (dig_P9) * p * p / 2147483648.0
    var2 = p * (dig_P8) / 32768.0
    pressure = (p + (var1 + var2 + (dig_P7)) / 16.0) / 100

    # Output data to screen
    return cTemp, pressure


#setting timeout for 30 minutes
timeout = time.time() + 60* 15

# Get ground pressure
ground_pressure_readings = []
for i in range(0,10):
    ground_pressure_readings.append(ReadTempAndPressure()[1])
ground_pressure = sum(ground_pressure_readings) / len(ground_pressure_readings)

def record_pressure():
    readings = []
    while True:
        temperature, pressure = ReadTempAndPressure()
        # Altitude = (R/g)*T*ln(Po/P)
        altitude = (287.058/9.81)*temperature*math.log(pressure/ground_pressure)
        temp_array = [temperature, pressure, altitude]
        readings.append(temp_array)
        time.sleep(0.05)
        # Writes in the values every 1 second (10 readings)
        if len(readings) == 10:
            # Writes the readings to the file
            with open("barometer_data.dat", "a") as file:
                for i in readings:
                    file.write("T:"+str(i[0])+"C; P:"+str(i[1])+"hPa; A:"+str(i[2])+"m" + "\n")
            readings = []  # Resets the 'readings' array
        if time.time() > timeout:
            break

'''
while True:

    temperature, pressure = ReadTempAndPressure()

    # Altitude = (R/g)*T*ln(Po/P)
    altitude = (287.058/9.81)*temperature*math.log(pressure/ground_pressure)

    temp_array = [temperature, pressure, altitude]

    readings.append(temp_array)
    time.sleep(0.05)

    # Writes in the values every 1 second (10 readings)
    if len(readings) == 10:

        # Writes the readings to the file
        with open("barometer_data.dat", "a") as file:
            for i in readings:
                file.write("T:"+i[0]+"C; P:"+i[1]+"hPa; A:"+i[2]+"m" + "\n")


        # Activate camera after apogee
        if readings[0][1] > readings[9][1]:
            Ascent = False
            Descent = True
            with open("video_start.txt", "w") as apogee:
                apogee.write("Going down!\n")

        readings = []  # Resets the 'readings' array


    if time.time() > timeout:
        break
'''
