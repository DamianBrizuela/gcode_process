from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer
from types import SimpleNamespace
from argparse import Namespace

file_gcode = 'code/texto_emma.gcode'
#analyzer = GcodeAnalyzer(file_gcode)
"""
def is_primitive(value):
    return isinstance(value, (str, int, float, bool, type(None)))

def process(obj, indent=0, file= None):
    prefix = " " * indent

    if isinstance(obj, SimpleNamespace):
        for key, value in obj.__dict__.items():
            if isinstance(value, SimpleNamespace):
                print(f"{prefix}{key.upper()}", file= file)
                process(value, indent + 2, file= file)
            elif isinstance(value, list):
                print(f"{prefix}{key.upper()}", file= file)
                for i, item in enumerate(value):
                    #print(f"{prefix}  - Item #{i}")
                    process(item, indent + 4, file= file)
            elif is_primitive(value):
                print(f"{prefix}{key}: {value}", file= file)
            else:
                print(f"{prefix}{key}: [complex object]", file= file)
                
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print(f"{prefix}- Item #{i}", file= file)
            process(item, indent + 2, file= file)
            
    elif is_primitive(obj):
        print(f"{prefix}{obj}", file= file)
        
    else:
        print(f"{prefix}[Unhandled type: {type(obj).__name__}]", file= file)
"""
#print(analyzer.process_settings())

def summary(_file_gcode, output_path= None):

    analyzer = GcodeAnalyzer(_file_gcode)
    if output_path is None:
        file_name = analyzer.get_file_name()
    else:
        file_name = output_path

    # Extraer datos clave
    gcode_summary = {
        "Tiempo estimado (min)": analyzer.get_time_minutes(),
        "Filamento usado (m)": analyzer.get_filament_used(),
        "Capas totales": analyzer.get_layer_count(),
        "Comandos M600 encontrados": analyzer.get_command_occurrences("M600")  
    }

    file_path = f'{file_name}.txt'
    with open(file_path, "w", encoding="utf-8") as file:
        summary = ''
        ident = ' '*3
        for key, value in gcode_summary.items():
            summary += f'{key}{ident} {value}\n'

        settings = analyzer.get_settings()
        summary += f'\nSETTINGS\n{settings}'
        file.write(summary)
    
    print('summary ok')

print('summary exec....')
summary(file_gcode)