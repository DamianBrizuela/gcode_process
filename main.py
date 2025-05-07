from lib.reader import reader

file_gcode = 'gcode/file_001.gcode'

obj = reader(file_gcode)
print(obj.global_quality.metadata.quality_type)