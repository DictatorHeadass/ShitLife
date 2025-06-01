from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QSize
import sys

from tabs.start_tab import StartTab
from tabs.stats_tab import StatsTab
from tabs.assets_tab import AssetsTab
from tabs.relationships_tab import RelationshipsTab
from tabs.job_tab import JobTab
from tabs.health_tab import HealthTab

from character import Character  # Your Character class handling player data
import sys
import traceback

def log_exception(exc_type, exc_value, exc_traceback):
    with open("log.txt", "a") as f:
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        f.write("\n" + "-"*60 + "\n")

# Hook the global exception handler
sys.excepthook = log_exception


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShitLife - Python Edition")
        self.resize(900, 600)
        
        # Create character
        self.character = Character()
        
        # Setup main widget and layout
        main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
        
        # Setup tabs
        self.tabs = QTabWidget()
        self.tabs.setIconSize(QSize(32, 32))
        
        # Initialize tabs with character data
        self.start_tab = StartTab(self.character, self)
        self.stats_tab = StatsTab(self.character)
        self.assets_tab = AssetsTab(self.character)
        self.relationships_tab = RelationshipsTab(self.character)
        self.job_tab = JobTab(self.character)
        self.health_tab = HealthTab(self.character)
        
        # Add tabs
        self.tabs.addTab(self.start_tab, "📝 Start")
        self.tabs.addTab(self.stats_tab, "📊 Stats")
        self.tabs.addTab(self.assets_tab, "🏠 Assets")
        self.tabs.addTab(self.relationships_tab, "❤️ Relationships")
        self.tabs.addTab(self.job_tab, "💼 Job")
        self.tabs.addTab(self.health_tab, "💪 Health")
        
        self.main_layout.addWidget(self.tabs)
        
        # Add Age Up button below tabs
        self.age_up_btn = QPushButton("⏳ Age Up")
        self.age_up_btn.clicked.connect(self.age_up)
        self.main_layout.addWidget(self.age_up_btn)
        self.age_up_btn.setEnabled(False)  # disable until name chosen
        
        # Disable all tabs except start at first
        for i in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(i, False)
        
        # Connect signal from start tab when name chosen to enable other tabs
        self.start_tab.name_chosen.connect(self.on_name_chosen)
    
    def on_name_chosen(self):
        # Enable all tabs and remove start tab
        for i in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(i, True)
        
        # Remove start tab
        start_index = self.tabs.indexOf(self.start_tab)
        if start_index != -1:
            self.tabs.removeTab(start_index)
        
        # Enable Age Up button
        self.age_up_btn.setEnabled(True)
        
        # Switch to stats tab after start
        self.tabs.setCurrentWidget(self.stats_tab)
    
    def age_up(self):
        self.character.age += 1
        
        # Passive boosts on age up
        self.character.health = min(100, self.character.health + 2)
        self.character.happiness = min(100, self.character.happiness + 3)
        
        # Show life event message if available
        if hasattr(self, 'random_life_event'):
            event_msg = self.random_life_event()
            if event_msg:
                QMessageBox.information(self, "Life Event", event_msg)
        
        # Update all tabs that depend on character state
        self.stats_tab.update_stats()
        self.assets_tab.update_assets()
        self.relationships_tab.update_relationships()
        self.job_tab.update_jobs()
        self.health_tab.update_health()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
