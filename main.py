from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer
from types import SimpleNamespace

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
for idx, values in (settings.__dict__.items()):
    print(f"\n[VALUE #{idx}]")
    if isinstance(values, SimpleNamespace):
        
        for section, data in values.__dict__.items():

            print(f"  [{section.upper()}]")
            for key, value in data.__dict__.items():
                print(f"    {key}: {value}")

    elif isinstance(values, list):
        for data in values:
                print(f'{data}')
    else:
         print('more...')