"""from view.calculator_view import CalculatorView
from controller.calculator_controller import CalculatorController
import sys
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    view = CalculatorView()
    controller = CalculatorController(view)

    view.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()"""


from PySide6.QtWidgets import QApplication
import sys

from view.calculator_view import CalculatorView
from controller.calculator_controller import CalculatorController

# Auto updater
from utils.updater import check_for_update, apply_update


def main():
    # Check for updates (non-blocking, safe)
    update_available, url = check_for_update()
    if update_available and url:
        print("New version available — downloading update...")
        apply_update(url)

    app = QApplication(sys.argv)

    view = CalculatorView()
    controller = CalculatorController(view)

    view.show()
    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()
