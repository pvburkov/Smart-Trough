import smbus

# Init bus
bus = smbus.SMBus(1)


class LPS331:
    """"LPS331 sensor reader class for Raspberry"""
    temperature = None
    pressure = None

    def __init__(self):
        # power up LPS331AP pressure sensor & set BDU bit
        bus.write_byte_data(0x5c, 0x20, 0b10000100)

    def get_temperature(self):
        Temp_LSB = bus.read_byte_data(0x5c, 0x2b)
        Temp_MSB = bus.read_byte_data(0x5c, 0x2c)

        # combine LSB & MSB
        count = (Temp_MSB << 8) | Temp_LSB

        # As value is negative convert 2's complement to decimal
        comp = count - (1 << 16)

        # calc temp according to data sheet
        return round(42.5 + (comp / 480.0), 2)

    def get_pressure(self):
        Pressure_XLB = bus.read_byte_data(0x5c, 0x28)
        Pressure_LSB = bus.read_byte_data(0x5c, 0x29)
        Pressure_MSB = bus.read_byte_data(0x5c, 0x2a)

        count = (Pressure_MSB << 16) | (Pressure_LSB << 8) | Pressure_XLB
        # comp = count - (1 << 24)
        # Pressure value is positive so just use value as decimal

        return round(count / 5461.33, 2)

    def read(self):
        # option to do a single read
        # write value 0b1 to register 0x21 on device at address 0x5d
        bus.write_byte_data(0x5c, 0x21, 0b1)
        self.temperature = self.get_temperature()
        self.pressure = self.get_pressure()

   
