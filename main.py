from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer
from types import SimpleNamespace
from argparse import Namespace

file_gcode = 'code/texto_emma.gcode'
analyzer = GcodeAnalyzer(file_gcode)

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

settings = analyzer.get_settings()
print(process(settings))

def summary(file_gcode, output_path= None):

    analyzer = GcodeAnalyzer(file_gcode)
    if output_path:
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
    with open(file_name, "w", encoding="utf-8") as f:

        ident = ' '*3
        for key, value in gcode_summary.items():
            print(f'{key}{ident} {value}', file= file_name)

        value_settings = analyzer.get_settings()
        #process_settings(value_settings, file=f)