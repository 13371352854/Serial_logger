import serial.tools.list_ports
import argparse
import sys
import time
import MySerial
import DataRecorder
import threading
import queue

VERSION = "1.0.0"

data_queue = queue.Queue()


class my_serial_thread(threading.Thread):
    def __init__(self,device,interval=0):
        super().__init__()
        self.device = device
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            data = self.device.receive_data()
            if data is not None:
                decoded_data = data.decode("utf-8")[1:-1]
                if decoded_data[-1] == "\n":
                    decoded_data = decoded_data[:-1]
                if decoded_data[-1] == "\r":
                    decoded_data = decoded_data[:-1]
                data_queue.put(decoded_data)
            time.sleep(self.interval)

    def stop_thread(self):
        self.running = False
        time.sleep(self.interval)


class my_data_recorder_thread(threading.Thread):
    def __init__(self,device,mode=0):
        super().__init__()
        self.device = device
        self.mode = mode
        self.running = True

    def run(self):
        while self.running:
            data = data_queue.get(block = True)
            if self.mode == 0:
                current_time = time.strftime("%H:%M:%S",time.localtime())
                print(f"{current_time}-->{data}")
                my_recorder.record_data(data)

    def stop_thread(self):
        self.running = False
        time.sleep(0.5)


if __name__ == '__main__':
    print('========================= Serial Logger =========================')
    parser = argparse.ArgumentParser(description = "Serial Logger")
    parser.add_argument("-p","--port",type = str,help = "COM Port")
    parser.add_argument("-b","--baud",type = int,help = "Baudrate, default = 115200 bps")
    parser.add_argument("-f","--file",type = str,help = "Log file name, default = <date>-<time>.csv")
    parser.add_argument("-v","--version",action = "store_true",help = "Show software version")
    parser.add_argument("-l","--list",action = "store_true",help = "List all the serial ports")
    args = parser.parse_args()
    if args.version:
        print(f"Software Version: {VERSION}")
        print(f"Author: XinYang")
        print(
            "Disclaimer: Any form of dissemination and use without permission is prohibited, breach at your own risk.")
        sys.exit(0)
    if args.list:
        serial_list = [port.device for port in serial.tools.list_ports.comports()]
        if len(serial_list) == 0:
            sys.exit('No serial devices found')
        print(f"COM List: {serial_list}")
        sys.exit(0)
    if args.port:
        serial_list = [port.device for port in serial.tools.list_ports.comports()]
        if len(serial_list) == 0:
            sys.exit('No serial devices found')
        if args.port not in serial_list:
            print(f"COM List: {serial_list}")
            sys.exit(f'device {args.port} not found')
        my_serial = MySerial.MyDeviceSerial(args.port,args.baud)
        if not my_serial.connect():
            sys.exit('Could not connect to serial port')
        my_recorder = DataRecorder.DataRecorder()
        my_recorder.add_new_file(args.file)
        data_thread = my_data_recorder_thread(device=my_recorder)
        data_thread.daemon = True
        data_thread.start()
        serial_thread = my_serial_thread(device=my_serial)
        serial_thread.daemon = True
        serial_thread.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit('Software exit by keyboard')
