import sys
from PySide6.QtWidgets import QApplication
from grid.grid import GridGui



if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = GridGui()
    gui.show()
    sys.exit(app.exec())
