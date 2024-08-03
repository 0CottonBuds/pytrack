from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

def setup_system_tray(app: QApplication, pytrack_main_window):

    if TYPE_CHECKING:
        assert isinstance(pytrack_main_window, App)

    # Create the icon
    icon = QIcon("Icons\icon.ico")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    activate_deactivate_main_loop_action = QAction(f"{pytrack_main_window.button_activate_deactivate_main_loop.text()} main loop")
    activate_deactivate_main_loop_action.triggered.connect(pytrack_main_window.activate_deactivate_main_loop)
    menu.addAction(activate_deactivate_main_loop_action)

    # Add a Quit option to the menu.
    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec()