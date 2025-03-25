import serial


class MyDeviceSerial:
    def __init__(self,port,baudrate=115200,bytesize=8,parity="N",stopbits=1.0,timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.ser = None

    def connect(self):
        self.ser = serial.Serial(self.port,self.baudrate,self.bytesize,self.parity,self.stopbits,self.timeout)
        if self.ser.is_open:
            return True
        else:
            return False

    def disconnect(self):
        if self.ser.is_open:
            self.ser.close()
            self.ser = None

    def send_data(self,data):
        if self.ser.is_open:
            self.ser.write(data)
            return True
        else:
            return False

    def receive_data(self,mode=0):
        if self.ser is None:
            return None
        if not self.ser.is_open:
            return None
        if mode == 0:
            data = self.ser.readline()
            if data == b'':
                return None
            return data
