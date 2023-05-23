from api_response import api_response
from yaml_handler import yaml_handler
from logging_handler import logging_handler
from uart import uart
from logo_ascii import logo_ascii

import sys, threading

class setup:
    def startup(self):
        self.thread_list={}
        self.serial_list={}
        self.settings()
        self.set_serialports()
        #self.http_response = http_response(self.logfile)
        self.api_response = api_response(self.uart_ports, self.logfile, self.serial_list)

    def thread_serial(self, serial_port, serial_name):
        task_reader = threading.Thread(
            name=f'Task_{serial_name}', 
            target=self.uart_ports.loop_reader,
            args=(serial_port, serial_name,))
        task_reader.start()
        self.thread_list[serial_name]={'thread':task_reader}
        self.serial_list[serial_name]={'serial_port':serial_port}

    def settings(self):
        #Get Setup Variables
        startup_file=yaml_handler()
        if not startup_file.content_file('startup.yaml'):sys.exit()
        self.setup_vars = startup_file.data
        #Set Logfile Config
        Logging_handler = logging_handler()
        if not Logging_handler.startup( 
            self.setup_vars['logging_handler']['format_template'],
            self.setup_vars['logging_handler']['path'],
            self.setup_vars['logging_handler']['max_bytes'],
            self.setup_vars['logging_handler']['num_backups'] ):sys.exit()
        self.logfile = Logging_handler.set_logger('root')
        logo = logo_ascii()
        self.logfile.info(logo.image())
    
    def set_serialports(self):
        #Set serial port
        self.uart_ports = uart(self.setup_vars['serialport']['timeout'],
                            self.setup_vars['serialport']['baudrate'],
                            self.logfile,
                            self.setup_vars['verify_commands'])
        if not self.uart_ports.get_list_ports(self.setup_vars['serialport']['ports']):sys.exit()
        for serial_name in self.uart_ports.list_ports:
            status, serial_port = self.uart_ports.connect(serial_name)
            if not status:continue
            self.thread_serial(serial_port, serial_name)
            if not self.uart_ports.write('BRD_DES', serial_port, serial_name):sys.exit()
            if not self.uart_ports.write('SEN_INP', serial_port, serial_name):sys.exit()
            if not self.uart_ports.write('REL_OUT', serial_port, serial_name):sys.exit()




