import falsificationMachine as fm

module = fm.m1()

cards_user = [[10,6]]
cards_dealer = [[10]]

module._calculate(cards_user, cards_dealer)
print(cards_user, cards_dealer)
print(module.falsify())
    
    