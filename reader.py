import json
import configparser
from io import StringIO
from types import SimpleNamespace

SETTINGS = ';SETTING_3 '
file_gcode = 'gcode/file_001.gcode'

def parse_ini_text(escaped_ini: str) -> dict:
    clean_ini = escaped_ini.replace("\\n", "\n")
    config = configparser.ConfigParser()
    config.read_file(StringIO(clean_ini))
    return {section: dict(config.items(section)) for section in config.sections()}

raw_text = ''

with open(file_gcode, 'r') as fh:
    
    for line_code in fh.readlines():
        if (SETTINGS in line_code):
            raw_text += line_code.replace(SETTINGS,'')

raw_txt = raw_text.replace('\n', '').replace('\r', '')

parsed_json = json.loads(raw_txt)

result = {}
for key, value in parsed_json.items():
    if isinstance(value, str):
        result[key] = parse_ini_text(value)
    elif isinstance(value, list):
        result[key] = [parse_ini_text(item) for item in value]

obj = json.loads(json.dumps(result), object_hook=lambda d: SimpleNamespace(**d))
print(obj.global_quality.metadata.quality_type)