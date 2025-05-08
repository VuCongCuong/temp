import sys
from PySide6.QtWidgets import QApplication
from ui.view import Window
from model.model import Model

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    model = Model() # Init the model
    window = Window(model) # Init the main window
    window.show()
    
    sys.exit(app.exec()) # Main event loop 