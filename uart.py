from flask import jsonify
import serial, sys
import serial.tools.list_ports
from time import sleep

class uart():
    def __init__(self, timeout, baudrate, logfile, ver_comm):
        self.timeout = timeout
        self.baudrate = baudrate
        self.data_collector = {}
        self.list_ports=[]
        self.logfile = logfile
        self.verify_commands = ver_comm

    def get_list_ports(self, ports):
        self.list_ports = ports
        all_ports = list(map(lambda x: x.device, serial.tools.list_ports.comports()))
        if not len(all_ports):
            self.logfile.error('List Ports is emphy.')
            return False
        return len(list(filter(lambda x: x in all_ports, ports))) == len(ports)

    def connect(self, serial_name):
        try:
            serial_port = serial.Serial(serial_name, self.baudrate)
            self.logfile.info(f'Port:{serial_name} success.')
            self.data_collector[serial_name]={'receive':[],'status':True}
            return True, serial_port
        except Exception as e:
            self.logfile.error(f'Serial Read Exception:{e}, Port:{serial_name}')
            return False, None

    def write(self, command, serial_port, serial_name, val=''):
        self.logfile.info(f'Data to write:{command + val}')
        try:
            serial_port.write(self.stringtobyte('\r' + command + val + '\n'))
            return self.verifyreceived(serial_name, command)
        except Exception as e:
            self.logfile.error(f'Serial Read Exception:{e}, Port:{serial_name}')
            return False
        
    def verifyreceived(self, serial_name, command):
        find = False
        for i in range(self.timeout):
            if self.verify_commands[command] in self.data_collector[serial_name]['receive']:
                self.data_collector[serial_name]['receive'].remove(self.verify_commands[command])
                find = True
                break
            else: sleep(0.1)
        if find:self.logfile.info('Verify Received PASS')
        else:self.logfile.error('Verify Received FAIL')
        return find
    
    def read(self, serial_port, serial_name):  
        try:  
            line = serial_port.readline()
            linestr = self.bytetostring(line)
            end = linestr.find('\n')
            start = linestr.find('\r')
            if (end != -1 and start != -1):
                msg = linestr[start + 1: end]
                return self.parse_message(msg, serial_name)
            else: 
                self.logfile.error(f'Serial Read, Wrong Syntax:{linestr}, Port:{serial_name}')
                return False
        except Exception as e:
            self.logfile.error(f'Serial Read Exception:{e}, Port:{serial_name}')
            return False
    
    def parse_message(self, msg, serial_name):
        self.logfile.info(f'Port:{serial_name}, MSG:{msg}')
        if msg.find('STA_INP') != -1:
            return self.parse_values(msg, serial_name, 'inputs')
        elif msg.find('STA_OUT') != -1:
            return self.parse_values(msg, serial_name, 'outputs')
        elif msg.find('MSG_DES') != -1:
            return self.parse_values(msg, serial_name, 'description')
        elif msg.find('MSG_FAI') != -1:
            self.logfile.error(f'Board FAILED, Port:{serial_name}')
            return False
        else:
            self.logfile.error(f'Message Received is Unknown, Port:{serial_name}')
            return False


    def parse_values(self, msg, serial_name, prop):
        try:
            set_values = msg.split('\t')[1]
            list_content = set_values.split(',')
            for data in list_content:
                data_split = data.split(':')
                if not prop in self.data_collector[serial_name]:
                    self.data_collector[serial_name][prop]={}
                self.data_collector[serial_name][prop][data_split[0]]=data_split[1] if prop=='description' else bool(int(data_split[1]))
            self.data_collector[serial_name]['receive'].append( msg.split('\t')[0])
            return True
        except Exception as e:
            self.logfile.error(f'Parse Exception:{e}')
            return False

    def loop_reader(self, serial_port, serial_name):
        while(True):
            if not self.read(serial_port, serial_name):
                self.data_collector[serial_name]['status']=False
            else:
                self.data_collector[serial_name]['status']=True

    def bytetostring(self, data):
        strData = data.decode('utf-8') 
        return strData

    def stringtobyte(self, data):
        byteData = data.encode('ascii', 'replace')
        return byteData

    def close(self, serial_port):
        serial_port.close() 
    

