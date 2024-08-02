import configparser

def read_config(path: str, section: str, key: str):
    """reads config file returns string of value"""
    config_obj = configparser.ConfigParser()
    config_obj.read(path)
    return config_obj[section][key]

def write_config(path: str, section: str, key: str, value: str):
    """writes at config file"""
    config_obj = configparser.ConfigParser()
    config_obj.add_section(section)
    config_obj.set(section, key, value)
    with open(path, "w") as config_file:
        config_obj.write(config_file)

def edit_config(path: str, section: str, key: str, value: str):
    """edits config file"""
    config_obj = configparser.ConfigParser()
    config_obj.read(path)
    section_to_edit = config_obj[section]
    section_to_edit[key] = value
    with open(path, "w") as config_file:
        config_obj.write(config_file)