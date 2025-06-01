from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox
)
import random

class JobTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.available_jobs = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("💼 Available Jobs")
        self.job_list = QListWidget()
        self.refresh_btn = QPushButton("🔄 Refresh Jobs")
        self.apply_btn = QPushButton("✅ Apply for Job")

        layout.addWidget(self.title)
        layout.addWidget(self.job_list)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.apply_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.refresh_btn.clicked.connect(self.refresh_job_list)
        self.apply_btn.clicked.connect(self.apply_for_job)

        self.refresh_job_list()

    def refresh_job_list(self):
        job_names = ["Cashier", "Barista", "Office Assistant", "Software Developer", "Teacher"]
        self.available_jobs = [
            {"title": job, "salary": random.randint(20000, 100000)} for job in job_names
        ]
        self.job_list.clear()
        for job in self.available_jobs:
            self.job_list.addItem(f"{job['title']} - ${job['salary']:,}/yr")

    def apply_for_job(self):
        selected = self.job_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No job selected", "Please select a job to apply.")
            return
        job = self.available_jobs[selected]
        self.character.job = job["title"]
        self.character.income = job["salary"]
        QMessageBox.information(self, "Job Accepted", f"You are now working as a {job['title']} making ${job['salary']:,}/yr.")
