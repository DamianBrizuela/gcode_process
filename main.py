from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer
from types import SimpleNamespace
from argparse import Namespace

file_gcode = 'code/texto_emma.gcode'

analyzer = GcodeAnalyzer(file_gcode)

# Extraer datos clave
gcode_summary = {
    "Tiempo estimado (min)": analyzer.get_time_minutes(),
    "Filamento usado (m)": analyzer.get_filament_used(),
    "Capas totales": analyzer.get_layer_count(),
    "Comandos M600 encontrados": analyzer.get_command_occurrences("M600")  
}

for key, value in gcode_summary.items():
    print(f'{key}\t\t: {value}')

print('*****************************************************************')

settings = analyzer.get_settings()



def process(obj, indent=0):
    prefix = " " * indent
    if isinstance(obj, SimpleNamespace):
        for key, value in obj.__dict__.items():
            print(f"{prefix} {key.upper()}")
            process(value, indent + 2)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            #print(f"{prefix}- Item #{i}")
            process(item, indent + 2)
    else:     
        print(f"{prefix}{obj} ({type(obj).__name__})")

process(settings)