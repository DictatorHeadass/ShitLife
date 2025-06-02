import random

class LifeEventSystem:
    def __init__(self, character):
        self.character = character
        
    def trigger_random_event(self):
        # 30% chance of an event happening each year
        if random.random() > 0.3:
            return None
            
        events = [
            ("Got a raise at work! Income increased by 10%", self.raise_income),
            ("Caught a cold, health -10", lambda: self.modify_health(-10)),
            ("Made a new friend! Happiness +15", lambda: self.modify_happiness(15)),
            ("Car broke down, lost $500", lambda: self.modify_money(-500)),
            ("Won a small lottery! +$2000", lambda: self.modify_money(2000)),
            ("Went on vacation, happiness +20, money -$1000", self.vacation_event),
            ("Had an argument with family, happiness -15", lambda: self.modify_happiness(-15)),
            ("Invested in crypto, market fluctuation", self.crypto_event),
            ("Random skill improvement!", self.skill_boost_event),
            ("Unexpected medical bill, -$1500", lambda: self.modify_money(-1500)),
            ("Found money on the street! +$100", lambda: self.modify_money(100)),
            ("Got food poisoning, health -15", lambda: self.modify_health(-15)),
            ("Attended a great party, happiness +10", lambda: self.modify_happiness(10)),
            ("Relationship improved with random person", self.relationship_boost),
            ("Work stress, happiness -10", lambda: self.modify_happiness(-10)),
        ]
        
        # Age-specific events
        if self.character.age >= 25 and not self.character.married:
            events.append(("Met someone special, started dating!", self.dating_event))
        
        if self.character.married and random.random() < 0.1:  # 10% chance if married
            events.append(("Had a baby! Happiness +25, Money -$5000", self.baby_event))
        
        if self.character.age >= 60:
            events.append(("Health checkup revealed good results! Health +10", lambda: self.modify_health(10)))
        
        event, effect = random.choice(events)
        effect()
        return event
    
    def raise_income(self):
        if self.character.income > 0:
            self.character.income = int(self.character.income * 1.1)
    
    def modify_health(self, amount):
        self.character.health = max(0, min(100, self.character.health + amount))
    
    def modify_happiness(self, amount):
        self.character.happiness = max(0, min(100, self.character.happiness + amount))
    
    def modify_money(self, amount):
        self.character.money = max(0, self.character.money + amount)
    
    def vacation_event(self):
        self.modify_happiness(20)
        self.modify_money(-1000)
    
    def crypto_event(self):
        # 60/40 chance to gain or lose money in crypto
        gain = random.choice([True, True, True, False, False])
        amount = random.randint(500, 3000)
        if gain:
            self.modify_money(amount)
        else:
            self.modify_money(-amount)
    
    def skill_boost_event(self):
        skill = random.choice(list(self.character.skills.keys()))
        boost = random.randint(3, 8)
        self.character.skills[skill] = min(100, self.character.skills[skill] + boost)
    
    def relationship_boost(self):
        person = random.choice(list(self.character.relationships.keys()))
        self.character.relationships[person]["level"] = min(100, 
            self.character.relationships[person]["level"] + random.randint(5, 15))
    
    def dating_event(self):
        self.character.relationships["Partner"]["level"] = min(100, 
            self.character.relationships["Partner"]["level"] + 20)
        self.modify_happiness(15)
    
    def baby_event(self):
        baby_name = f"Child {len(self.character.children) + 1}"
        self.character.children.append(baby_name)
        self.modify_happiness(25)
        self.modify_money(-5000)
        self.character.add_achievement("Parent")
