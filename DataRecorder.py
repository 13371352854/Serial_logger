import os
import socket
import time
import csv


class DataRecorder:
    def __init__(self):
        self.date = None
        self.time = None
        self.csv_file_path = None
        self.csv_file_name = None
        self.seq_num = 0

    def add_new_file(self,file_name=None):
        self.date = time.strftime("%Y%m%d",time.localtime())
        self.time = time.strftime("%H%M%S",time.localtime())
        self.csv_file_path = os.path.join(os.getcwd(),"CSV_Files")
        if file_name is None:
            self.csv_file_name = f"{self.date}-{self.time}.csv"
        else:
            self.csv_file_name = f"{file_name}-{self.time}.csv"
        self.seq_num = 0
        if not os.path.exists(self.csv_file_path):
            os.mkdir(self.csv_file_path)
        with open(os.path.join(self.csv_file_path,self.csv_file_name),'w',newline = '') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["===================== Data Recorder ====================="])
            csv_writer.writerow([f"Hostname:{socket.gethostname()}"])
            csv_writer.writerow([f"Date_Time:{self.date}_{self.time}"])
            csv_writer.writerow(["========================================================="])
            csv_writer.writerow(["Sequence Number","Time","Data"])

    def record_data(self,data_list):
        with open(os.path.join(self.csv_file_path,self.csv_file_name),'a+',newline = '') as f:
            csv_writer = csv.writer(f)
            self.seq_num = self.seq_num + 1
            current_time = time.strftime("%H%M%S",time.localtime())
            if isinstance(data_list,str):
                data_list_buffer = [self.seq_num,current_time] + [data_list]
            elif isinstance(data_list,list):
                data_list_buffer = [self.seq_num,current_time] + data_list
            else:
                data_list_buffer = [self.seq_num,current_time] + [data_list]
            csv_writer.writerow(data_list_buffer)

    def get_file_date(self):
        return self.date

    def get_file_time(self):
        return self.time

    def get_file_name(self):
        return self.csv_file_name
