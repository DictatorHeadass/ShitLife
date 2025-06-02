from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox, QHBoxLayout
)

class EducationTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        
        self.init_ui()
        self.update_education()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Current education status
        self.current_education_label = QLabel()
        layout.addWidget(self.current_education_label)
        
        # Available education options
        self.education_list = QListWidget()
        layout.addWidget(QLabel("Available Education Options:"))
        layout.addWidget(self.education_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.enroll_btn = QPushButton("🎓 Enroll")
        self.study_btn = QPushButton("📚 Study (Improve Intelligence)")
        
        btn_layout.addWidget(self.enroll_btn)
        btn_layout.addWidget(self.study_btn)
        layout.addLayout(btn_layout)
        
        # Skills improvement section
        skills_layout = QVBoxLayout()
        skills_layout.addWidget(QLabel("Skill Development:"))
        
        skill_btn_layout = QHBoxLayout()
        self.read_btn = QPushButton("📖 Read Books (+Intelligence)")
        self.socialize_btn = QPushButton("🗣️ Socialize (+Charisma)")
        self.workout_btn = QPushButton("🏋️ Workout (+Fitness)")
        self.create_btn = QPushButton("🎨 Create Art (+Creativity)")
        self.business_btn = QPushButton("💼 Business Course (+Business)")
        
        skill_btn_layout.addWidget(self.read_btn)
        skill_btn_layout.addWidget(self.socialize_btn)
        skill_btn_layout.addWidget(self.workout_btn)
        skill_btn_layout.addWidget(self.create_btn)
        skill_btn_layout.addWidget(self.business_btn)
        
        skills_layout.addLayout(skill_btn_layout)
        layout.addLayout(skills_layout)
        
        # Skills display
        self.skills_label = QLabel()
        layout.addWidget(self.skills_label)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.enroll_btn.clicked.connect(self.enroll_education)
        self.study_btn.clicked.connect(self.study)
        self.read_btn.clicked.connect(lambda: self.improve_skill("Intelligence"))
        self.socialize_btn.clicked.connect(lambda: self.improve_skill("Charisma"))
        self.workout_btn.clicked.connect(lambda: self.improve_skill("Fitness"))
        self.create_btn.clicked.connect(lambda: self.improve_skill("Creativity"))
        self.business_btn.clicked.connect(lambda: self.improve_skill("Business"))
    
    def update_education(self):
        # Update current education status
        education_names = {
            1: "High School Graduate",
            2: "Community College Student/Graduate",
            3: "University Student/Graduate", 
            4: "Graduate School Student/Graduate"
        }
        current_ed = education_names.get(self.character.education_level, "Unknown")
        self.current_education_label.setText(f"Current Education: {current_ed}")
        
        # Update available education options
        self.education_list.clear()
        for level, info in self.character.education_options.items():
            if level > self.character.education_level:
                cost = info["cost"]
                req_int = info["req_intelligence"]
                duration = info["duration"]
                can_afford = self.character.money >= cost
                meets_req = self.character.skills["Intelligence"] >= req_int
                
                status = "✅" if (can_afford and meets_req) else "❌"
                item_text = f"{status} {info['name']} - ${cost:,} (Req: {req_int} Intelligence, {duration} years)"
                self.education_list.addItem(item_text)
        
        # Update skills display
        skills_text = "Skills:\n"
        for skill, value in self.character.skills.items():
            skills_text += f"{skill}: {value}/100\n"
        self.skills_label.setText(skills_text)
    
    def enroll_education(self):
        current_item = self.education_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an education option.")
            return
        
        # Parse the selected education level
        item_text = current_item.text()
        if "Community College" in item_text:
            level = 2
        elif "University" in item_text:
            level = 3
        elif "Graduate School" in item_text:
            level = 4
        else:
            return
        
        if self.character.start_education(level):
            education_name = self.character.education_options[level]["name"]
            QMessageBox.information(self, "Enrolled!", f"You've enrolled in {education_name}!")
            self.character.education = education_name
            
            # Add achievement
            if level == 3:
                self.character.add_achievement("College Graduate")
            elif level == 4:
                self.character.add_achievement("Graduate Degree")
            
            self.update_education()
        else:
            QMessageBox.warning(self, "Cannot Enroll", "You don't meet the requirements or can't afford this education.")
    
    def study(self):
        # Studying improves intelligence but costs time and a bit of money
        cost = 50
        if self.character.money < cost:
            QMessageBox.warning(self, "No Money", "You need $50 to buy study materials.")
            return
        
        self.character.money -= cost
        improvement = random.randint(2, 5)
        self.character.skills["Intelligence"] = min(100, self.character.skills["Intelligence"] + improvement)
        
        QMessageBox.information(self, "Study Session", f"You studied hard! Intelligence +{improvement}")
        self.update_education()
    
    def improve_skill(self, skill_name):
        # Each skill improvement costs money and has different effects
        costs = {
            "Intelligence": 100,
            "Charisma": 75,
            "Fitness": 50,
            "Creativity": 80,
            "Business": 120
        }
        
        cost = costs[skill_name]
        if self.character.money < cost:
            QMessageBox.warning(self, "Insufficient Funds", f"You need ${cost} to improve {skill_name}.")
            return
        
        self.character.money -= cost
        improvement = random.randint(3, 8)
        self.character.skills[skill_name] = min(100, self.character.skills[skill_name] + improvement)
        
        # Side effects
        if skill_name == "Fitness":
            self.character.health = min(100, self.character.health + 5)
        elif skill_name == "Charisma":
            self.character.happiness = min(100, self.character.happiness + 3)
        
        QMessageBox.information(self, "Skill Improved", f"{skill_name} improved by {improvement} points!")
        self.update_education()

import random