import json
import configparser
from io import StringIO
from types import SimpleNamespace

SETTINGS = ';SETTING_3 '
COMMENTS = ';'
# file_gcode = 'gcode/file_001.gcode'

def settings_reader(file, code):
    """
        Leer el archivo y recupera los settings del mismo
    """

    def parse_ini_text(escaped_ini: str) -> dict:
        clean_ini = escaped_ini.replace("\\n", "\n")
        config = configparser.ConfigParser()
        config.read_file(StringIO(clean_ini))
        return {section: dict(config.items(section)) for section in config.sections()}

    raw_text = ''

    with open(file, 'r') as fh:
         for line_code in fh:
            if line_code.startswith(code):
                raw_text += line_code[len(code):].strip()

    raw_txt = raw_text.replace('\n', '').replace('\r', '')

    parsed_json = json.loads(raw_txt)

    result = {}
    for key, value in parsed_json.items():
        if isinstance(value, str):
            result[key] = parse_ini_text(value)
        elif isinstance(value, list):
            result[key] = [parse_ini_text(item) for item in value]

    obj = json.loads(json.dumps(result), object_hook=lambda d: SimpleNamespace(**d))

    return obj

def comments_reader(file):
    raw_text = ''
    with open(file, 'r') as fh:

        for line_code in fh.readlines():
            if (COMMENTS in line_code):
                raw_text += line_code.replace(COMMENTS,'')

    # raw_txt = raw_text.replace('\n', '').replace('\r', '')
    raw_txt = raw_text.replace('\r', '')

    return raw_txt

def retrieve_code(file, code: str):

    raw_text = ''

    with open(file, 'r') as fh:
         for line_code in fh:
            if line_code.startswith(code):
                raw_text += line_code[len(code):].strip()

    raw_txt = raw_text.replace('\n', '').replace('\r', '')
    return raw_txt


def parse_SETTIMGS3(file):
    contenido_json = ""
    with open(file) as fh:
        for line in fh:
            if line.startswith(";SETTING_3"):
                contenido_json += line[len(";SETTING_3 "):].strip()
    settings = json.loads(contenido_json)
    print(settings)