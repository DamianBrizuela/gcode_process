from lib.reader import reader
from lib.reader.gcode_analyzer import GcodeAnalyzer

file_gcode = 'gcode/file_002.gcode'

analyzer = GcodeAnalyzer(file_gcode)

# Extraer datos clave
gcode_summary = {
    "Tiempo estimado (min)": analyzer.get_time_minutes(),
    "Filamento usado (m)": analyzer.get_filament_used(),
    "Capas totales": analyzer.get_layer_count(),
    "Comandos M600 encontrados": analyzer.get_command_occurrences("M600"),
    "Configuracion": analyzer.get_settings(),
    
}
print(gcode_summary)