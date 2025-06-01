from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class RelationshipsTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character

        self.init_ui()
        self.update_relationships()

    def init_ui(self):
        layout = QVBoxLayout()

        self.relationships_list = QListWidget()
        self.relationships_list.setSelectionMode(QListWidget.SingleSelection)

        self.detail_label = QLabel("Select a relationship to see details.")
        self.detail_label.setWordWrap(True)

        btn_layout = QHBoxLayout()
        self.improve_btn = QPushButton("Improve Relationship")
        self.worsen_btn = QPushButton("Worsen Relationship")
        btn_layout.addWidget(self.improve_btn)
        btn_layout.addWidget(self.worsen_btn)

        self.improve_btn.clicked.connect(self.improve_relationship)
        self.worsen_btn.clicked.connect(self.worsen_relationship)

        layout.addWidget(QLabel("Your Relationships:"))
        layout.addWidget(self.relationships_list)
        layout.addWidget(self.detail_label)
        layout.addLayout(btn_layout)

        self.relationships_list.currentItemChanged.connect(self.show_relationship_detail)

        self.setLayout(layout)

    def update_relationships(self):
        """Refresh the relationships list and update details."""
        self.refresh_list()
        self.show_relationship_detail(self.relationships_list.currentItem())

    def refresh_list(self):
        self.relationships_list.clear()
        for name, info in self.character.relationships.items():
            level = info.get("level", 50)
            self.relationships_list.addItem(f"{name} - Level: {level}")

    def show_relationship_detail(self, current, previous=None):
        if not current:
            self.detail_label.setText("Select a relationship to see details.")
            return

        text = current.text()
        name = text.split(" - ")[0]
        info = self.character.relationships.get(name, {})
        level = info.get("level", 50)
        description = info.get("description", "No description available.")
        self.detail_label.setText(f"{name}\nLevel: {level}\n{description}")

    def improve_relationship(self):
        current = self.relationships_list.currentItem()
        if not current:
            return
        name = current.text().split(" - ")[0]
        self.character.relationships[name]["level"] = min(100, self.character.relationships[name].get("level", 50) + 10)
        self.update_relationships()

    def worsen_relationship(self):
        current = self.relationships_list.currentItem()
        if not current:
            return
        name = current.text().split(" - ")[0]
        self.character.relationships[name]["level"] = max(0, self.character.relationships[name].get("level", 50) - 10)
        self.update_relationships()
