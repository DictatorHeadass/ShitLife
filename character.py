class Character:
    def __init__(self):
        self.name = ""
        self.age = 18
        self.money = 10000
        self.health = 100
        self.happiness = 50
        self.education = "None"
        self.job = None
        self.income = 0
        
        # Owned assets start empty
        self.assets = {
            "House": {},
            "Car": {},
            "Crypto": {},
        }
        
        # Static data for all possible assets and their base prices
        self.assets_data = {
            "House": {
                "Mansion": 500000,
                "Villa": 250000,
                "Apartment": 100000,
            },
            "Car": {
                "Sports Car": 60000,
                "SUV": 40000,
                "Sedan": 25000,
            },
            "Crypto": {
                "Bitcoin": 30000,
                "Ethereum": 2000,
                "Dogecoin": 0.25,
            }
        }
        
        self.relationships = {
            "Mom": {"level": 70, "description": "Your caring mother."},
            "Dad": {"level": 65, "description": "Your strict father."},
            "Best Friend": {"level": 80, "description": "Your loyal friend."},
            "Partner": {"level": 50, "description": "Your significant other."}
        }
