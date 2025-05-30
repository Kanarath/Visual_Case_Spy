# visual_case_spy/main.py
import sys
from PySide6.QtWidgets import QApplication
# from PySide6.QtCore import Qt # No es directamente necesario aquí, pero MainWindow lo usa
from visual_case_spy.ui.main_window import MainWindow # Asegúrate de que esta ruta sea correcta

print("DEBUG: main.py - Script starting")

def run_app():
    print("DEBUG: run_app() - Entered")
    try:
        app = QApplication(sys.argv)
        print("DEBUG: run_app() - QApplication created")

        window = MainWindow()
        print("DEBUG: run_app() - MainWindow instance created")

        window.show()
        print("DEBUG: run_app() - MainWindow.show() called")

        print("DEBUG: run_app() - Calling app.exec()")
        exit_code = app.exec() # Almacenamos el código de salida
        print(f"DEBUG: run_app() - app.exec() finished with code: {exit_code}")
        sys.exit(exit_code)

    except Exception as e:
        print(f"FATAL ERROR in run_app(): {e}")
        import traceback
        traceback.print_exc() # Imprime el traceback completo del error

if __name__ == "__main__":
    print("DEBUG: main.py - __main__ block entered")
    run_app()
    print("DEBUG: main.py - Script finished (esto solo se verá si app.exec() termina y sys.exit no detiene todo)")