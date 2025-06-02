from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QSize
import sys
import json
import os

from tabs.start_tab import StartTab
from tabs.stats_tab import StatsTab
from tabs.assets_tab import AssetsTab
from tabs.relationships_tab import RelationshipsTab
from tabs.job_tab import JobTab
from tabs.health_tab import HealthTab
from tabs.education_tab import EducationTab
from tabs.activities_tab import ActivitiesTab
from tabs.achievements_tab import AchievementsTab

from character import Character
from utils import LifeEventSystem
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
        self.setWindowTitle("ShitLife - Enhanced Python Edition")
        self.resize(1100, 700)
        
        # Create character
        self.character = Character()
        
        # Initialize life event system
        self.life_events = LifeEventSystem(self.character)
        
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
        self.education_tab = EducationTab(self.character)
        self.activities_tab = ActivitiesTab(self.character)
        self.achievements_tab = AchievementsTab(self.character)
        
        # Add tabs
        self.tabs.addTab(self.start_tab, "📝 Start")
        self.tabs.addTab(self.stats_tab, "📊 Stats")
        self.tabs.addTab(self.assets_tab, "🏠 Assets")
        self.tabs.addTab(self.relationships_tab, "❤️ Relationships")
        self.tabs.addTab(self.job_tab, "💼 Job")
        self.tabs.addTab(self.health_tab, "💪 Health")
        self.tabs.addTab(self.education_tab, "🎓 Education")
        self.tabs.addTab(self.activities_tab, "🎲 Activities")
        self.tabs.addTab(self.achievements_tab, "🏆 Achievements")
        
        self.main_layout.addWidget(self.tabs)
        
        # Add control buttons
        button_layout = QVBoxLayout()
        
        # Age Up button
        self.age_up_btn = QPushButton("⏳ Age Up")
        self.age_up_btn.clicked.connect(self.age_up)
        button_layout.addWidget(self.age_up_btn)
        self.age_up_btn.setEnabled(False)  # disable until name chosen
        
        # Save/Load buttons
        save_load_layout = QVBoxLayout()
        self.save_btn = QPushButton("💾 Save Game")
        self.load_btn = QPushButton("📁 Load Game")
        self.save_btn.clicked.connect(self.save_game)
        self.load_btn.clicked.connect(self.load_game)
        save_load_layout.addWidget(self.save_btn)
        save_load_layout.addWidget(self.load_btn)
        
        button_layout.addLayout(save_load_layout)
        self.main_layout.addLayout(button_layout)
        
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
        
        # Enable buttons
        self.age_up_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.load_btn.setEnabled(True)
        
        # Switch to stats tab after start
        self.tabs.setCurrentWidget(self.stats_tab)
    
    def age_up(self):
        old_age = self.character.age
        self.character.age += 1
        
        # Apply yearly income if employed
        if self.character.job and self.character.income > 0:
            yearly_income = self.character.income
            self.character.money += yearly_income
            
        # Business income
        for business, qty in self.character.assets.get("Business", {}).items():
            if business in self.character.assets_data["Business"]:
                # Businesses generate 10-20% of their value annually
                base_value = self.character.assets_data["Business"][business]
                income = int(base_value * qty * (0.1 + (self.character.skills["Business"] / 1000)))
                self.character.money += income
        
        # Passive changes on age up
        self.character.health = max(0, min(100, self.character.health + 2 - (self.character.age * 0.1)))
        self.character.happiness = min(100, self.character.happiness + 3)
        
        # Age-based skill degradation (very slow)
        if self.character.age > 40:
            for skill in self.character.skills:
                if skill == "Fitness":
                    self.character.skills[skill] = max(0, self.character.skills[skill] - 0.5)
        
        # Check for milestones and achievements
        self.check_age_achievements()
        
        # Random life event
        event_msg = self.life_events.trigger_random_event()
        if event_msg:
            QMessageBox.information(self, "Life Event", event_msg)
        
        # Check for death conditions
        if self.character.health <= 0:
            self.handle_death()
            return
        
        # Update all tabs that depend on character state
        self.update_all_tabs()
    
    def check_age_achievements(self):
        age = self.character.age
        achievements = []
        
        if age == 21:
            achievements.append("Legal Adult!")
        elif age == 30:
            achievements.append("Dirty Thirty")
        elif age == 50:
            achievements.append("Half Century")
        elif age == 65:
            achievements.append("Senior Citizen")
        elif age == 100:
            achievements.append("Centenarian!")
        
        # Net worth achievements
        net_worth = self.character.get_net_worth()
        if net_worth >= 1000000 and "Millionaire" not in self.character.achievements:
            achievements.append("Millionaire")
        elif net_worth >= 10000000 and "Multi-Millionaire" not in self.character.achievements:
            achievements.append("Multi-Millionaire")
        
        for achievement in achievements:
            self.character.add_achievement(achievement)
    
    def handle_death(self):
        final_age = self.character.age
        net_worth = self.character.get_net_worth()
        
        death_msg = f"💀 Game Over! 💀\n\n"
        death_msg += f"You lived to {final_age} years old.\n"
        death_msg += f"Final net worth: ${net_worth:,}\n"
        death_msg += f"Achievements earned: {len(self.character.achievements)}\n\n"
        death_msg += "Thanks for playing ShitLife!"
        
        QMessageBox.information(self, "Game Over", death_msg)
        self.close()
    
    def update_all_tabs(self):
        """Update all tabs that depend on character state"""
        self.stats_tab.update_stats()
        self.assets_tab.update_assets()
        self.relationships_tab.update_relationships()
        self.job_tab.update_jobs()
        self.health_tab.update_health()
        self.education_tab.update_education()
        self.activities_tab.update_activities()
        self.achievements_tab.update_achievements()
    
    def save_game(self):
        try:
            save_data = {
                "name": self.character.name,
                "age": self.character.age,
                "money": self.character.money,
                "health": self.character.health,
                "happiness": self.character.happiness,
                "education": self.character.education,
                "job": self.character.job,
                "income": self.character.income,
                "skills": self.character.skills,
                "achievements": self.character.achievements,
                "criminal_record": self.character.criminal_record,
                "married": self.character.married,
                "spouse_name": self.character.spouse_name,
                "children": self.character.children,
                "education_level": self.character.education_level,
                "assets": self.character.assets,
                "relationships": self.character.relationships
            }
            
            with open("savegame.json", "w") as f:
                json.dump(save_data, f, indent=4)
            
            QMessageBox.information(self, "Game Saved", "Your game has been saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        try:
            if not os.path.exists("savegame.json"):
                QMessageBox.warning(self, "Load Error", "No save file found!")
                return
            
            with open("savegame.json", "r") as f:
                save_data = json.load(f)
            
            # Load character data
            self.character.name = save_data.get("name", "")
            self.character.age = save_data.get("age", 18)
            self.character.money = save_data.get("money", 10000)
            self.character.health = save_data.get("health", 100)
            self.character.happiness = save_data.get("happiness", 50)
            self.character.education = save_data.get("education", "High School")
            self.character.job = save_data.get("job", None)
            self.character.income = save_data.get("income", 0)
            self.character.skills = save_data.get("skills", self.character.skills)
            self.character.achievements = save_data.get("achievements", [])
            self.character.criminal_record = save_data.get("criminal_record", 0)
            self.character.married = save_data.get("married", False)
            self.character.spouse_name = save_data.get("spouse_name", "")
            self.character.children = save_data.get("children", [])
            self.character.education_level = save_data.get("education_level", 1)
            self.character.assets = save_data.get("assets", self.character.assets)
            self.character.relationships = save_data.get("relationships", self.character.relationships)
            
            # Update all tabs
            self.update_all_tabs()
            
            QMessageBox.information(self, "Game Loaded", "Your game has been loaded successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Failed to load game: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
