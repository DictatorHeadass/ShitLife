from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
)

class HealthTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        
        self.init_ui()
        self.update_status()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.health_label = QLabel()
        self.happiness_label = QLabel()
        
        self.exercise_btn = QPushButton("Exercise (+10 Health)")
        self.eat_healthy_btn = QPushButton("Eat Healthy (+5 Health)")
        self.meditate_btn = QPushButton("Meditate (+10 Happiness)")
        self.sleep_btn = QPushButton("Sleep Well (+15 Health & Happiness)")
        
        layout.addWidget(self.health_label)
        layout.addWidget(self.happiness_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.exercise_btn)
        btn_layout.addWidget(self.eat_healthy_btn)
        btn_layout.addWidget(self.meditate_btn)
        btn_layout.addWidget(self.sleep_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.exercise_btn.clicked.connect(self.exercise)
        self.eat_healthy_btn.clicked.connect(self.eat_healthy)
        self.meditate_btn.clicked.connect(self.meditate)
        self.sleep_btn.clicked.connect(self.sleep_well)
    
    def update_status(self):
        self.health_label.setText(f"Health: {self.character.health}%")
        self.happiness_label.setText(f"Happiness: {self.character.happiness}%")
    
    def exercise(self):
        self.character.health = min(100, self.character.health + 10)
        self.update_status()
    
    def eat_healthy(self):
        self.character.health = min(100, self.character.health + 5)
        self.update_status()
    
    def meditate(self):
        self.character.happiness = min(100, self.character.happiness + 10)
        self.update_status()
    
    def sleep_well(self):
        self.character.health = min(100, self.character.health + 15)
        self.character.happiness = min(100, self.character.happiness + 15)
        self.update_status()
