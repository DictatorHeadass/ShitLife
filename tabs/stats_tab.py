from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatsTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        
        self.layout = QVBoxLayout()
        
        self.name_label = QLabel(f"Name: {self.character.name or 'N/A'}")
        self.age_label = QLabel(f"Age: {self.character.age}")
        self.money_label = QLabel(f"Money: ${self.character.money}")
        self.health_label = QLabel(f"Health: {self.character.health}%")
        self.happiness_label = QLabel(f"Happiness: {self.character.happiness}%")
        self.education_label = QLabel(f"Education: {self.character.education}")
        self.job_label = QLabel(f"Job: {self.character.job or 'Unemployed'}")
        
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.money_label)
        self.layout.addWidget(self.health_label)
        self.layout.addWidget(self.happiness_label)
        self.layout.addWidget(self.education_label)
        self.layout.addWidget(self.job_label)
        
        self.setLayout(self.layout)
    
    def update_stats(self):
        self.name_label.setText(f"Name: {self.character.name}")
        self.age_label.setText(f"Age: {self.character.age}")
        self.money_label.setText(f"Money: ${self.character.money}")
        self.health_label.setText(f"Health: {self.character.health}%")
        self.happiness_label.setText(f"Happiness: {self.character.happiness}%")
        self.education_label.setText(f"Education: {self.character.education}")
        self.job_label.setText(f"Job: {self.character.job or 'Unemployed'}")
