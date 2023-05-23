class api_response:
    def __init__(self, uart_ports, logfile, serial_list):
        self.uart_ports=uart_ports
        self.logfile = logfile
        self.serial_list =  serial_list

    def set_relay_value(self, ipaddr, content):
        self.logfile.info(f'Ip Address:{ipaddr}')
        sta, resp = self.wrongformat(content, 'str', 'serial_name')
        if not sta:return resp
        sta, resp = self.wrongformat(content, 'int', 'number')
        if not sta:return resp
        sta, resp = self.wrongformat(content, 'bool', 'mode')
        if not sta:return resp

        mode = 'REL_CLO' if content['mode'] else 'REL_OPE'
        if not self.uart_ports.write(mode, self.serial_list[content['serial_name']]['serial_port'], content['serial_name'], str(content['number'])):
            return {'status': False, 'msg':mode}
        return {'status':True, 
               'data':self.uart_ports.data_collector[content['serial_name']]['outputs'], 
               'match':content['mode']==self.uart_ports.data_collector[content['serial_name']]['outputs']['OUT_REL{}'.format(content['number'])]}

    
    def get_relay_out(self, ipaddr, content):
        self.logfile.info(f'Ip Address:{ipaddr}')
        sta, resp = self.wrongformat(content, 'str', 'serial_name')
        if not sta:return resp
        if not self.uart_ports.write('REL_OUT', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'REL_OUT'}
        return {'status':True, 'data':self.uart_ports.data_collector[content['serial_name']]['outputs']}
    
    def get_sensor_inp(self, ipaddr, content):
        self.logfile.info(f'Ip Address:{ipaddr}')
        sta, resp = self.wrongformat(content, 'str', 'serial_name')
        if not sta:return resp
        if not self.uart_ports.write('SEN_INP', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'SEN_INP'}
        return {'status':True, 'data':self.uart_ports.data_collector[content['serial_name']]['inputs']}


    def get_board_description(self, ipaddr, content):
        self.logfile.info(f'Ip Address:{ipaddr}')
        sta, resp = self.wrongformat(content, 'str', 'serial_name')
        if not sta:return resp
        if not self.uart_ports.write('BRD_DES', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'BRD_DES'}
        return {'status':True, 'data':self.uart_ports.data_collector[content['serial_name']]['description']}


    def get_complete(self, ipaddr, content):
        self.logfile.info(f'Ip Address:{ipaddr}')
        sta, resp = self.wrongformat(content, 'str', 'serial_name')
        if not sta:return resp
        if not self.uart_ports.write('BRD_DES', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'BRD_DES'}
        if not self.uart_ports.write('SEN_INP', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'SEN_INP'}
        if not self.uart_ports.write('REL_OUT', self.serial_list[content['serial_name']]['serial_port'], content['serial_name']):
            return {'status': False, 'msg':'REL_OUT'}
        else:return {'status': True, 'data':self.uart_ports.data_collector[content['serial_name']]}

    def wrongformat(self, data, type_, propertie):
        response = {}
        if(data.get(propertie) == None):
            response['status']=False
            response['msg'] = 'propertie ' + propertie + ' not found.'
            self.logfile.error('propertie ' + propertie + ' not found.')
            return False, response
        
        if(type_ == 'int'):
            if(type(data[propertie]) is not int):
                response['status']=False
                response['msg'] = 'It has wrong value format in ' + propertie + ' =' + str(type(data[propertie]))
                self.logfile.error('It has wrong value format in ' + propertie + ' =' + str(type(data[propertie])))
                return False, response
            else: return True, None

        if(type_ == 'str'):
            if(type(data[propertie]) is not str):
                response['status']=False
                response['msg'] = 'It has wrong value format in ' + propertie + ' =' + str(type(data[propertie]))
                self.logfile.error('It has wrong value format in ' + propertie + ' =' + str(type(data[propertie])))
                return False, response
            else: return True, None
        
        if(type_ == 'bool'):
            if(type(data[propertie]) is not bool):
                response['status']=False
                response['msg'] = 'It has wrong value format in ' + propertie + ' =' + str(type(data[propertie]))
                self.logfile.error('It has wrong value format in ' + propertie + ' =' + str(type(data[propertie])))
                return False, response
            else: return True, None
            
        if(type_ == 'json'):
            return True, None

        else:    
            response['status']=False
            response['msg'] = 'type known ' + type
            self.logfile.error('type known ' + type)
            return False, response
