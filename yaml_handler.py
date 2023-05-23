import yaml

class yaml_handler:
    def content_file(self, file_name):
        try:
            file = open(file_name, 'r')
            self.data = yaml.load(file, Loader=yaml.FullLoader)
            return True
        except Exception as e:
            print(f'Yaml File Failed during open, Exception:{e}')
            return False