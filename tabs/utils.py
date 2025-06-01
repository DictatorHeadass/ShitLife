import random

def random_life_event(self):
    events = [
        ("Got a raise at work! Income +10%", lambda: self.raise_income(0.1)),
        ("Caught a cold, health -10%", lambda: self.modify_health(-10)),
        ("Made a new friend! Happiness +15", lambda: self.modify_happiness(15)),
        ("Car broke down, lost $500", lambda: self.modify_money(-500)),
        ("Won a small lottery! +$2000", lambda: self.modify_money(2000)),
        ("Went on vacation, happiness +20, money -$1000", lambda: (self.modify_happiness(20), self.modify_money(-1000))),
        ("Had an argument, happiness -15", lambda: self.modify_happiness(-15)),
        ("Invested in crypto, potential gain or loss", self.crypto_event),
        # add more cool events
    ]
    event, effect = random.choice(events)
    effect()
    return event

def raise_income(self, percent):
    self.character.income = int(self.character.income * (1 + percent))

def modify_health(self, amount):
    self.character.health = max(0, min(100, self.character.health + amount))

def modify_happiness(self, amount):
    self.character.happiness = max(0, min(100, self.character.happiness + amount))

def modify_money(self, amount):
    self.character.money = max(0, self.character.money + amount)

def crypto_event(self):
    # 50/50 chance to gain or lose money in crypto
    gain = random.choice([True, False])
    amount = random.randint(500, 2000)
    if gain:
        self.modify_money(amount)
    else:
        self.modify_money(-amount)
