class Character:
    def __init__(self):
        self.name = ""
        self.age = 18
        self.money = 10000
        self.health = 100
        self.happiness = 50
        self.education = "High School"
        self.job = None
        self.income = 0
        
        # New attributes
        self.skills = {
            "Intelligence": 50,
            "Charisma": 50,
            "Fitness": 50,
            "Creativity": 50,
            "Business": 50
        }
        
        self.achievements = []
        self.criminal_record = 0  # 0 = clean, higher = more crimes
        self.married = False
        self.spouse_name = ""
        self.children = []
        self.education_level = 1  # 1=High School, 2=College, 3=University, 4=Graduate
        
        # Owned assets start empty
        self.assets = {
            "House": {},
            "Car": {},
            "Crypto": {},
            "Business": {},
        }
        
        # Enhanced static data for all possible assets and their base prices
        self.assets_data = {
            "House": {
                "Mansion": 500000,
                "Villa": 250000,
                "Apartment": 100000,
                "Condo": 150000,
                "Penthouse": 750000,
            },
            "Car": {
                "Sports Car": 60000,
                "SUV": 40000,
                "Sedan": 25000,
                "Luxury Car": 100000,
                "Motorcycle": 15000,
                "Truck": 35000,
            },
            "Crypto": {
                "Bitcoin": 30000,
                "Ethereum": 2000,
                "Dogecoin": 0.25,
                "Litecoin": 100,
                "Cardano": 0.50,
                "Solana": 20,
            },
            "Business": {
                "Restaurant": 75000,
                "Tech Startup": 100000,
                "Retail Store": 50000,
                "Real Estate Agency": 80000,
                "Consulting Firm": 60000,
            }
        }
        
        self.relationships = {
            "Mom": {"level": 70, "description": "Your caring mother."},
            "Dad": {"level": 65, "description": "Your strict father."},
            "Best Friend": {"level": 80, "description": "Your loyal friend."},
            "Partner": {"level": 50, "description": "Your significant other."}
        }
        
        # Education options
        self.education_options = {
            2: {"name": "Community College", "cost": 5000, "duration": 2, "req_intelligence": 30},
            3: {"name": "University", "cost": 25000, "duration": 4, "req_intelligence": 60},
            4: {"name": "Graduate School", "cost": 40000, "duration": 2, "req_intelligence": 80}
        }
    
    def add_achievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
    
    def get_net_worth(self):
        asset_value = 0
        for category, assets in self.assets.items():
            for asset, quantity in assets.items():
                if category in self.assets_data and asset in self.assets_data[category]:
                    asset_value += self.assets_data[category][asset] * quantity
        return self.money + asset_value
    
    def can_afford_education(self, level):
        if level not in self.education_options:
            return False
        cost = self.education_options[level]["cost"]
        intelligence_req = self.education_options[level]["req_intelligence"]
        return self.money >= cost and self.skills["Intelligence"] >= intelligence_req
    
    def start_education(self, level):
        if self.can_afford_education(level):
            cost = self.education_options[level]["cost"]
            self.money -= cost
            self.education_level = level
            return True
        return False
