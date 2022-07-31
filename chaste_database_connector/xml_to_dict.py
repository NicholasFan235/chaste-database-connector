import re

def xml_to_dict(xml:str):
    return _XmlToDict(xml).data

class _XmlToDict:
    def __init__(self, xml:str):
        self.xml = xml.replace('\n', '').replace('\t', '').replace(' ', '')
        self.data = None
        self.data = self.convert_helper(0, len(self.xml), self.data)
    
    def convert_helper(self, i:int, j:int, data):
        if self.xml[i] != '<':
            return self.xml[i:j]
        
        while i < j:
            key = self.xml[i+1:i+self.xml[i:j].find('>')]
            if key[0] == '!':
                i += len(key)+2
                continue
            end_loc = self.xml[i:j].find(f'</{key}>')
            assert end_loc > 0, f'Cannot close <{key}>'

            if data is None: data = {}
            assert type(data) == dict, f"Invalid datatype in converted data: {type(self.data)}"
            if key in data:
                if type(data[key]) == list:
                    data[key].append(None)
                else:
                    data[key] = [data[key], None]
                data[key][-1] = self.convert_helper(i+len(key)+2, i+end_loc, data[key][-1])
            else:
                data[key] = None
                data[key] = self.convert_helper(i+len(key)+2, i+end_loc, data[key])
            i += end_loc + len(key) + 3
        return data





