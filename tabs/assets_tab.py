from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QSpinBox,
    QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class AssetsTab(QWidget):
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character

        # Set up asset base data & prices
        self.assets_data = self.character.assets_data
        self.current_prices = {
            "House": {name: price for name, price in self.assets_data["House"].items()},
            "Car": {name: price for name, price in self.assets_data["Car"].items()},
            "Crypto": {name: price for name, price in self.assets_data["Crypto"].items()},
        }

        self.price_history = {
            "House": {name: [price] for name, price in self.current_prices["House"].items()},
            "Car": {name: [price] for name, price in self.current_prices["Car"].items()},
            "Crypto": {name: [price] for name, price in self.current_prices["Crypto"].items()},
        }

        self.init_ui()
        self.update_prices()
        self.refresh_owned()
        self.init_graph()
        self.start_price_timer()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        left_panel = QVBoxLayout()
        
        # Houses
        self.house_group = QGroupBox("🏠 Houses")
        self.house_list = QListWidget()
        self.house_qty = QSpinBox()
        self.house_qty.setMinimum(1)
        self.house_buy_btn = QPushButton("Buy")
        self.house_sell_btn = QPushButton("Sell")
        self.house_price_label = QLabel()
        self.house_buy_btn.clicked.connect(lambda: self.buy_asset("House"))
        self.house_sell_btn.clicked.connect(lambda: self.sell_asset("House"))
        self.house_group.setLayout(self.create_asset_layout(self.house_list, self.house_qty, self.house_price_label, self.house_buy_btn, self.house_sell_btn))
        
        # Cars
        self.car_group = QGroupBox("🚗 Cars")
        self.car_list = QListWidget()
        self.car_qty = QSpinBox()
        self.car_qty.setMinimum(1)
        self.car_buy_btn = QPushButton("Buy")
        self.car_sell_btn = QPushButton("Sell")
        self.car_price_label = QLabel()
        self.car_buy_btn.clicked.connect(lambda: self.buy_asset("Car"))
        self.car_sell_btn.clicked.connect(lambda: self.sell_asset("Car"))
        self.car_group.setLayout(self.create_asset_layout(self.car_list, self.car_qty, self.car_price_label, self.car_buy_btn, self.car_sell_btn))
        
        # Crypto
        self.crypto_group = QGroupBox("🪙 Crypto")
        self.crypto_list = QListWidget()
        self.crypto_qty = QSpinBox()
        self.crypto_qty.setMinimum(1)
        self.crypto_buy_btn = QPushButton("Buy")
        self.crypto_sell_btn = QPushButton("Sell")
        self.crypto_price_label = QLabel()
        self.crypto_buy_btn.clicked.connect(lambda: self.buy_asset("Crypto"))
        self.crypto_sell_btn.clicked.connect(lambda: self.sell_asset("Crypto"))
        self.crypto_group.setLayout(self.create_asset_layout(self.crypto_list, self.crypto_qty, self.crypto_price_label, self.crypto_buy_btn, self.crypto_sell_btn))
        
        left_panel.addWidget(self.house_group)
        left_panel.addWidget(self.car_group)
        left_panel.addWidget(self.crypto_group)
        
        # Owned assets on bottom left
        self.owned_group = QGroupBox("Owned Assets")
        self.owned_list = QListWidget()
        owned_layout = QVBoxLayout()
        owned_layout.addWidget(self.owned_list)
        self.owned_group.setLayout(owned_layout)
        left_panel.addWidget(self.owned_group)

        main_layout.addLayout(left_panel, 3)
        
        # Graph canvas will be added inside owned_group layout dynamically
        
        self.setLayout(main_layout)
        
        self.refresh_asset_lists()
        self.update_price_label("House")
        self.update_price_label("Car")
        self.update_price_label("Crypto")

        # Update price labels when selection changes
        self.house_list.currentItemChanged.connect(lambda: self.update_price_label("House"))
        self.car_list.currentItemChanged.connect(lambda: self.update_price_label("Car"))
        self.crypto_list.currentItemChanged.connect(lambda: self.update_price_label("Crypto"))
    
    def create_asset_layout(self, list_widget, qty_spinbox, price_label, buy_btn, sell_btn):
        layout = QVBoxLayout()
        layout.addWidget(list_widget)
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Quantity:"))
        qty_layout.addWidget(qty_spinbox)
        layout.addLayout(qty_layout)
        layout.addWidget(price_label)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(buy_btn)
        btn_layout.addWidget(sell_btn)
        layout.addLayout(btn_layout)
        return layout
    
    def refresh_asset_lists(self):
        self.house_list.clear()
        self.house_list.addItems(self.assets_data["House"].keys())
        self.car_list.clear()
        self.car_list.addItems(self.assets_data["Car"].keys())
        self.crypto_list.clear()
        self.crypto_list.addItems(self.assets_data["Crypto"].keys())

    def refresh_owned(self):
        self.owned_list.clear()
        for cat, assets in self.character.assets.items():
            for name, qty in assets.items():
                self.owned_list.addItem(f"{cat} - {name}: {qty}")
    
    def update_price_label(self, category):
        list_widget = {
            "House": self.house_list,
            "Car": self.car_list,
            "Crypto": self.crypto_list
        }[category]
        item = list_widget.currentItem()
        if not item:
            return
        name = item.text()
        price = self.current_prices[category][name]
        label = {
            "House": self.house_price_label,
            "Car": self.car_price_label,
            "Crypto": self.crypto_price_label
        }[category]
        label.setText(f"Current Price: ${price:,.2f}")

    def buy_asset(self, category):
        list_widget = {
            "House": self.house_list,
            "Car": self.car_list,
            "Crypto": self.crypto_list
        }[category]
        item = list_widget.currentItem()
        if not item:
            return
        name = item.text()
        qty = {
            "House": self.house_qty.value(),
            "Car": self.car_qty.value(),
            "Crypto": self.crypto_qty.value()
        }[category]
        price = self.current_prices[category][name] * qty
        if self.character.money < price:
            QMessageBox.warning(self, "Insufficient funds", "You don't have enough money!")
            return
        self.character.money -= price
        self.character.assets[category][name] = self.character.assets[category].get(name, 0) + qty
        self.refresh_owned()

    def sell_asset(self, category):
        list_widget = {
            "House": self.house_list,
            "Car": self.car_list,
            "Crypto": self.crypto_list
        }[category]
        item = list_widget.currentItem()
        if not item:
            return
        name = item.text()
        qty = {
            "House": self.house_qty.value(),
            "Car": self.car_qty.value(),
            "Crypto": self.crypto_qty.value()
        }[category]
        owned_qty = self.character.assets[category].get(name, 0)
        if owned_qty < qty:
            QMessageBox.warning(self, "Not enough assets", "You don't own that many to sell!")
            return
        price = self.current_prices[category][name] * qty
        self.character.assets[category][name] = owned_qty - qty
        if self.character.assets[category][name] == 0:
            del self.character.assets[category][name]
        self.character.money += price
        self.refresh_owned()

    def update_prices(self):
        def fluctuate(base, low_pct, high_pct):
            change_pct = random.uniform(low_pct, high_pct)
            return max(base * (1 + change_pct), 1)  # Prevent price <=0
        
        for cat in self.assets_data:
            for asset, base_price in self.assets_data[cat].items():
                if cat == "House":
                    self.current_prices[cat][asset] = fluctuate(base_price, -0.05, 0.05)
                elif cat == "Car":
                    self.current_prices[cat][asset] = fluctuate(base_price, -0.03, 0.03)
                elif cat == "Crypto":
                    self.current_prices[cat][asset] = fluctuate(base_price, -0.2, 0.2)

    def init_graph(self):
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.owned_group.layout().addWidget(self.canvas)
        
        self.selected_category = "House"
        self.selected_asset = list(self.assets_data["House"].keys())[0]

        self.house_list.currentItemChanged.connect(lambda: self.update_graph("House"))
        self.car_list.currentItemChanged.connect(lambda: self.update_graph("Car"))
        self.crypto_list.currentItemChanged.connect(lambda: self.update_graph("Crypto"))

        self.update_graph("House")

    def start_price_timer(self):
        self.price_timer = QTimer()
        self.price_timer.timeout.connect(self.periodic_price_update)
        self.price_timer.start(5000)

    def periodic_price_update(self):
        self.update_prices()
        for cat in self.assets_data:
            for asset in self.assets_data[cat]:
                self.price_history[cat][asset].append(self.current_prices[cat][asset])
        self.refresh_owned()
        self.update_price_label(self.selected_category)
        self.update_graph(self.selected_category)

    def update_graph(self, category):
        list_widget = {
            "House": self.house_list,
            "Car": self.car_list,
            "Crypto": self.crypto_list
        }[category]
        item = list_widget.currentItem()
        if not item:
            return
        asset = item.text()
        self.selected_category = category
        self.selected_asset = asset

        self.ax.clear()
        prices = self.price_history[category][asset]
        self.ax.plot(prices, label=f"{asset} Price")
        self.ax.set_title(f"{asset} Price History")
        self.ax.set_xlabel("Time (ticks)")
        self.ax.set_ylabel("Price ($)")
        self.ax.legend()
        self.canvas.draw()

    def update_assets(self):
        """
        Called from main.py when aging up to refresh all asset-related UI and data.
        """
        self.refresh_owned()
        self.update_price_label(self.selected_category)
        self.update_graph(self.selected_category)
