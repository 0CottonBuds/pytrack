from PySide6.QtWidgets import QApplication
from Helpers.config_helper import read_config

def change_stylesheet(object, theme: str, app:QApplication):
    '''Changes the stylesheet of Qapplication.
    Params:
        object: any = Target object 
        style : str = Theme to use.
        app : QApplication = QApplication object that you want to apply the stylesheet.
    '''
    _theme = open(f"Assets/Themes/{theme}_theme.css","r").read()
    app.setStyleSheet(_theme)
    print(f"Changed theme to {theme} theme.")
    object.update()

def get_themes():
    """Returns a list of themes written in config file.
    
    Return:
        list[str] = names for themes.
    """
    themes = str(read_config("config.ini", "App", "themes"))
    themes = themes.split(", ")
    default_theme= read_config("config.ini", "App", "theme")
    themes.remove(default_theme)
    themes.insert(0, default_theme)
    return themes

