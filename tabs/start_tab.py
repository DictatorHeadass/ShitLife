from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class StartTab(QWidget):
    name_chosen = pyqtSignal()
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Welcome! Please enter your name to start your life journey 👶:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name here")
        
        self.start_button = QPushButton("Start Life")
        self.start_button.clicked.connect(self.on_start_clicked)
        
        layout.addWidget(self.label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)
    
    def on_start_clicked(self):
        name = self.name_input.text().strip()
        if name:
            self.character.name = name
            self.name_chosen.emit()
        else:
            self.label.setText("You gotta enter a name first! Try again 🫡")
