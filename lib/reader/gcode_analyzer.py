import re
import json
from typing import Optional, List, Dict, Tuple
import configparser
from io import StringIO
from types import SimpleNamespace
from argparse import Namespace

class GcodeAnalyzer:
    def __init__(self, path: str):
        self.path = path
        self.lines = self._read_lines()
        self.metadata = self._parse_metadata()
        self.commands = self._find_commands(["M600", "M109", "M104"])

    def _read_lines(self) -> List[str]:
        with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()

    def _parse_metadata(self) -> Dict[str, Optional[str]]:
        meta = {}
        setting_3_json = ""

        for line in self.lines:
            if line.startswith(";TIME:"):
                meta["time_s"] = int(line.split(":")[1])
            elif line.startswith(";Filament used:"):
                meta["filament_m"] = float(line.split(":")[1].replace("m", "").strip())
            elif line.startswith(";LAYER_COUNT:"):
                meta["layer_count"] = int(line.split(":")[1])
            elif line.startswith(";SETTING_3"):
                setting_3_json += line.replace(";SETTING_3 ", "").strip()

        if setting_3_json:
            try:
                meta["settings"] = json.loads(setting_3_json)
            except json.JSONDecodeError:
                meta["settings"] = None

        return meta

    def _find_commands(self, command_list: List[str]) -> Dict[str, List[Tuple[int, str]]]:
        results = {cmd: [] for cmd in command_list}
        for idx, line in enumerate(self.lines):
            for cmd in command_list:
                if cmd in line:
                    results[cmd].append((idx + 1, line.strip()))
        return results

    def get_time_minutes(self) -> Optional[int]:
        return self.metadata.get("time_s", 0) // 60 if self.metadata.get("time_s") else None

    def get_filament_used(self) -> Optional[float]:
        return self.metadata.get("filament_m")
    
    def get_layer_count(self) -> Optional[int]:
        return self.metadata.get("layer_count")
    
    def get_file_name(self) -> Optional[int]:
        return self._get_settings().global_quality.general.name
    
    def get_command_occurrences(self, command: str) -> List[Tuple[int, str]]:
        return self.commands.get(command, [])

    def _get_settings(self) -> Optional[dict]:
        parsed_json = self.metadata.get("settings")

        def parse_ini_text(escaped_ini: str) -> dict:
            clean_ini = escaped_ini.replace("\\n", "\n")
            config = configparser.ConfigParser()
            config.read_file(StringIO(clean_ini))
            return {section: dict(config.items(section)) for section in config.sections()}
        
        #parsed_json = json.loads(settings)
        result = {}
        for key, value in parsed_json.items():
            if isinstance(value, str):
                result[key] = parse_ini_text(value)
            elif isinstance(value, list):
                result[key] = [parse_ini_text(item) for item in value]
    
        obj = json.loads(json.dumps(result), object_hook=lambda d: SimpleNamespace(**d))

        def namespace_to_dict(obj_to_dict):
            if isinstance(obj_to_dict, Namespace):
                return {k: namespace_to_dict(v) for k, v in vars(obj_to_dict).items()}
            elif isinstance(obj_to_dict, list):
                return [namespace_to_dict(item) for item in obj_to_dict]
            else:
                return obj_to_dict
            
        return namespace_to_dict(obj)

    def get_settings(self):
        settings = self._get_settings()

        def is_primitive(value):
            return isinstance(value, (str, int, float, bool, type(None)))

        def process(obj, indent=0, lines= None):
            if lines is None:
                lines = []

            prefix = " " * indent

            if isinstance(obj, SimpleNamespace):
                for key, value in obj.__dict__.items():
                    if isinstance(value, SimpleNamespace):
                        lines.append(f"{prefix}{key.upper()}")
                        process(value, indent + 2, lines)
                    elif isinstance(value, list):
                        lines.append(f"{prefix}{key.upper()}")
                        for i, item in enumerate(value):
                            process(item, indent + 4, lines)
                    elif is_primitive(value):
                        lines.append(f"{prefix}{key}: {value}")
                    else:
                        lines.append(f"{prefix}{key}: [complex object]")
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    lines.append(f"{prefix}- Item #{i}")
                    process(item, indent + 2, lines)
                    
            elif is_primitive(obj):
                lines.append(f"{prefix}{obj}")
                
            else:
                lines.append(f"{prefix}[Unhandled type: {type(obj).__name__}]")

            return lines
        lines = process(settings)
        return '\n'.join(lines)

        
