from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer
from types import SimpleNamespace
from argparse import Namespace
import os

file_gcode = 'code/texto_emma.gcode'

def summary(_file_gcode, output_path= None):

    analyzer = GcodeAnalyzer(_file_gcode)
    if output_path is None:
        file_name = os.path.basename(_file_gcode)
    else:
        file_name = output_path

    gcode_summary = {
        "Nombre del archivo": file_name,
        "Nombre de configuracion": analyzer.get_config_name(),
        "Tiempo estimado (min)": analyzer.get_time_minutes(),
        "Filamento usado (m)": analyzer.get_filament_used(),
        "Capas totales": analyzer.get_layer_count(),
        "Comandos M600 encontrados": analyzer.get_command_occurrences("M600")  
    }
    path = f'settings'
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = f'{path}/{file_name}.txt'
    with open(file_path, "w", encoding="utf-8") as file:
        summary = ''
        ident = ' '*3
        for key, value in gcode_summary.items():
            summary += f'{key}{ident} {value}\n'

        settings = analyzer.get_settings()
        summary += f'\nSETTINGS\n{settings}'
        file.write(summary)

summary(file_gcode)