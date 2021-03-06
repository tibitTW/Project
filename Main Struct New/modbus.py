from pymodbus.client.sync import ModbusTcpClient
from constant import TORCH_SPEED_VALUE, SOLDER_SPEED_VALUE
from constant import MENUAL_MODE, AUTO_MODE
from constant import GUN_VOLTAGE, GUN_AMP
from constant import SET_GUN_SPEED, SET_SOLDER_SPEED


class PLC:
    def __init__(self, ip: str = '192.168.1.87'):
        self.__ip = ip
        self.__client = ModbusTcpClient(self.__ip)

    def is_connect(self):
        return self.__client.connect()

    def disconnect(self):
        if self.__client.connect():
            self.__client.close()
            print(f'Client at {self.__ip} closed.')

    def get_mode_status(self):
        if self.__client.connect():
            if self.__client.read_coils(0xB000+4).bits[0]:
                return MENUAL_MODE
            elif self.__client.read_coils(0x2000+21).bits[0]:
                return AUTO_MODE
        else:
            return -1

    def setting_value(self):
        if not self.__client.connect():
            return 0

        return self.__client.read_coils(0x2000+4).bits[0]

    def setting_value_end(self):
        try:
            return self.__client.read_coils(0x2000+5).bits[0]
        except Exception:
            return 0

    def is_setting_value(self, id: int):
        if not self.__client.connect():
            return

        try:
            if id == SET_GUN_SPEED:
                return self.__client.read_coils(0x2000+13).bits[0]
            elif id == SET_SOLDER_SPEED:
                return self.__client.read_coils(0x2000+14).bits[0]
        except Exception as e:
            print(e)
            return -1

    def read_value(self, id: int):
        if not self.__client.connect():
            return

        try:
            if id == GUN_VOLTAGE:
                return self.__client.read_holding_registers(100).registers[0]
            elif id == GUN_AMP:
                return self.__client.read_holding_registers(200).registers[0]

        except Exception as e:
            print(e)
            return -1

    def write_value(self, id: int, value):
        try:
            if id == TORCH_SPEED_VALUE:
                self.__client.write_register(10, int(value*2//3))
            elif id == SOLDER_SPEED_VALUE:
                self.__client.write_register(12, int((value + 415.70) * 0.947))

        except Exception:
            print(int(value*400))

    def check_value(self, id: int):
        if not self.__client.connect():
            return -1

        try:
            if id == TORCH_SPEED_VALUE:
                return self.__client.read_holding_registers(10).registers[0]
            elif id == SOLDER_SPEED_VALUE:
                return self.__client.read_holding_registers(12).registers[0]

        except Exception as e:
            print(e)
            return -1

    def send_start_autorun(self):
        try:
            return self.__client.read_coils(0xB000+5).bits[0]
        except Exception:
            return -1

    def send_shutdown(self):
        try:
            if self.__client.read_coils(0x2000+20).bits[0]:
                return True
            else:
                return False
        except Exception:
            pass

    def reset(self):
        try:
            if self.__client.read_coils(0x2000+200).bits[0]:
                return True

            return False
        except Exception:
            return
