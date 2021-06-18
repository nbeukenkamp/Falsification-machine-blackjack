# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 12:59:53 2021

@author: nbeuk
"""

class _module (object):    
    
    """
    A module must support some kind falsification function that produces a falsifying question.  
    """  
    def __init__(self):  
        self.message = None
    
    def falsify(self, *any_input, verbose=False):
        self.analysis = None


class m1 (_module):
    """
    This module uses the probability of winning a game of blackjack to produce 2 falsifying questions for a specific round of blackjack.
    """  
    def __init__(self):
        """This function initializes the module and what is needed to calculate the probability of winning"""
        super().__init__()
        self.message = "Did you consider '"
        self.options = ["stand","hit","double down","surrender"]
        self.chances = [0,0,0,0]
        self.deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7
                     ,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10
                     ,10,10,10,10,10,10,"ace","ace","ace","ace",]
        
    def _calculate(self, cards_user, cards_dealer, sort=False):
        """This function uses the cards of the user and the dealer to calculate the probability of winning for both the stand and the hit option"""
        self.cards_user = cards_user 
        self.cards_dealer = cards_dealer
       
        self.deck.remove(self.cards_user[0])
        self.deck.remove(self.cards_user[1])
        self.deck.remove(self.cards_dealer[0])
        
        for i in self.options:
            if i == "stand":
                for k in self.cards_user:
                    if "ace" in self.cards_user:
                        j = self.cards_user.index("ace")
                        self.cards_user[j] = 11
                points_user = sum(self.cards_user)
                points_dealer = self.cards_dealer[0]
                if points_user > 21:
                        points_user -= 10
                if points_dealer == "ace":
                    points_dealer = 11
                deck = self.deck.copy()
                winrate, possibilities = self.chance_win(points_user, points_dealer, deck)
                self.chances[0] = winrate/possibilities
            elif i == "hit":
                contains_ace = 0
                starting_ace = 0
                for k in cards_user:
                    if 11 == k:
                        j = self.cards_user.index(11)
                        self.cards_user[j] = "ace"
                        starting_ace += 1
                temp_chances = []
                for j in range(len(self.deck)):
                    contains_ace = starting_ace
                    for l in range(len(self.cards_user)):
                        if self.cards_user[l] == "ace":
                            self.cards_user[l] = 11
                    points_user = sum(self.cards_user)
                    if points_user > 21 and contains_ace > 0:
                            m = self.cards_user.index(11)
                            self.cards_user[m] = 1
                            contains_ace -= 1
                    points_user = sum(self.cards_user)
                    if self.deck[j] == "ace" and (points_user + 11) < 22:
                        next_card = 11
                        contains_ace += 1
                    elif self.deck[j] == "ace" and (points_user + 11) > 21:
                        next_card = 1
                    else:
                        next_card = self.deck[j]
                    points_user += next_card
                    if points_user > 21 and contains_ace > 0:
                        points_user -= 10
                        contains_ace -= 1
                    deck = self.deck.copy()
                    del deck[j]
                    winrate, possibilities = self.chance_win(points_user, points_dealer, deck)
                    temp_chances.append(winrate/possibilities)
                self.chances[1] = sum(temp_chances)/len(temp_chances)
            elif i == "double down":
                self.chances[2] = self.chances[1]
            elif i == "surrender":
                self.chances[3] = 0
    
    def chance_win(self, points_user, points_dealer, deck):
        """This function uses the current points of the user, the points of the dealer and the deck (where the cards of the user and the
        dealer have been removed from) to see in which scenarios the user would win."""
        winrate = 0
        possibilities = 0
        contains_ace = 0
        start_points_dealer = points_dealer
        starting_ace = 0
        if points_dealer == 11:
            contains_ace = 1
            starting_ace = contains_ace
        for i in deck:
            temp_win = 0
            temp_pos = 1
            temp_deck = deck.copy()
            temp_deck.remove(i)
            if i == "ace":
                contains_ace += 1
                i = 11
            points_dealer += i
            if contains_ace > 0 and points_dealer > 21:
                points_dealer -= 10
                contains_ace -= 1
            if points_user > 21:
                winrate += 0
            elif points_user == 21:
                winrate += 1
            elif points_dealer < 17:
                for j in temp_deck:
                    temp2_win = 0
                    temp2_pos = 1
                    temp2_deck = temp_deck.copy()
                    temp2_deck.remove(j)
                    if j == "ace":
                        contains_ace += 1
                        j = 11
                    points_dealer += j
                    if contains_ace > 0 and points_dealer > 21:
                        points_dealer -= 10
                        contains_ace -= 1
                    if points_dealer < 17:
                        for m in temp2_deck:
                            temp3_win = 0
                            temp3_pos = 1
                            temp3_deck = temp2_deck.copy()
                            temp3_deck.remove(m)
                            if m == "ace":
                                contains_ace += 1
                                m = 11
                            points_dealer += m
                            if contains_ace > 0 and points_dealer > 21:
                                points_dealer -= 10
                                contains_ace -= 1
                            if points_dealer < 17:
                                for l in temp3_deck:
                                    temp4_win = 0
                                    temp4_pos = 1
                                    temp4_deck = temp3_deck.copy()
                                    temp4_deck.remove(l)
                                    if l == "ace":
                                        contains_ace += 1
                                        l = 11
                                    points_dealer += l
                                    if contains_ace > 0 and points_dealer > 21:
                                        points_dealer -= 10
                                        contains_ace -= 1
                                    if points_dealer < 17:
                                        for n in temp4_deck:
                                            if n == "ace":
                                                contains_ace += 1
                                                n = 11
                                            points_dealer += l
                                            if contains_ace > 0 and points_dealer > 21:
                                                points_dealer -= 10
                                                contains_ace -= 1
                                            if (points_dealer > 21 and points_user < 22) or (points_user >= points_dealer and points_user < 22):
                                                temp4_win += 1
                                            temp4_pos += 1
                                            points_dealer -= n
                                    elif (points_dealer > 21 and points_user < 22) or (points_user >= points_dealer and points_user < 22):
                                        temp3_win += 1
                                    temp3_win += (temp4_win/temp4_pos)
                                    temp3_pos += 1
                                    points_dealer -= l
                            elif (points_dealer > 21 and points_user < 22) or (points_user >= points_dealer and points_user < 22):
                                temp2_win += 1
                            temp2_win += (temp3_win/temp3_pos)
                            temp2_pos += 1
                            points_dealer -= m
                    elif (points_dealer > 21 and points_user < 22) or (points_user >= points_dealer and points_user < 22):
                        temp_win += 1
                    temp_win += (temp2_win/temp2_pos)
                    temp_pos += 1
                    points_dealer -= j
                    contains_ace = starting_ace
            elif (points_dealer > 21 and points_user < 22) or (points_user >= points_dealer and points_user < 22):
                winrate += 1
            winrate += (temp_win/temp_pos)           
            possibilities += 1
            points_dealer = start_points_dealer
            if self.cards_dealer[0] == 11:
                contains_ace = 1
            else:
                contains_ace = 0
        return winrate, possibilities
    
        
    def evaluate(self, option):
        """This function produces the feedback for each option in the blackjack game"""
        if option == "stand":
            self.analysis = "That there is an approximately ", round(100*(self.chances[0]),1), "% chance of winning when you choose to stand."
        if option == "hit":
            self.analysis = "That there is an approximately ", round(100*(self.chances[1]),1), "% chance of winning when you choose to take an extra card."
        if option == "double down":
            self.analysis = "That there is an approximately ", round(100*(self.chances[2]),1), "% chance of winning double your stakes when you choose to take an extra card."
        if option == "surrender":
            self.analysis = "That there is an approximately ", round(100*(self.chances[3]),1), "% chance of winning when you choose to surrender."
        return self.analysis
                
        
    def falsify(self, verbose=True):
        """This function falsifies the feedback for every given option"""
        for option in self.options:
            self.analysis = "Module 1 says: Did you consider the following?\n", self.evaluate(option)
            print(self.analysis)
        
        if verbose:
            return self.analysis

    