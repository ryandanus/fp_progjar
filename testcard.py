import random

class Card(object):
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit
        self.showing = True
    def __repr__(self):
        if self.showing:
            return str(self.name) + " of " + self.suit
        else:
            return "Card"

class StandardDeck(object):
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
        values = {"Two" : 2,
                  "Three" : 3,
                  "Four" : 4,
                  "Five" : 5,
                  "Six" : 6,
                  "Seven" : 7,
                  "Eight" : 8,
                  "Nine" : 9,
                  "Ten" : 10,
                  "Jack" : 11,
                  "Queen" : 12,
                  "King" : 13,
                  "Ace" : 14,}

        for name in values:
            for suit in suits:
                self.cards.append(Card(name, values[name], suit))

    def shuffle(self):
        random.shuffle(self.cards)
        print("Deck Shuffled")

    def __repr__(self):
        return "Standard deck of cards: {} cards remaining".format(len(self.cards))

    def deal(self):
        return self.cards.pop(0)


class Player(object):
    def __init__(self, cards):
        self.cards = []

    def cardCount(self):
        pass


class PokerScorer(object):
    def __init__(self, cards):
        self.cards = cards
        self.values = []
        for card in self.cards:
            self.values.append(card.value)
        self.suits = []
        for card in self.cards:
            self.suits.append(card.suit)

    def __repr__(self):
        return self.cards

    def suits(self):
        suits = []
        for card in self.cards:
            suits.append(card.suit)
        print(set(suits))
        return list(set(suits))

    def royal(self):
        values = []
        for card in self.cards:
            values.append(card.value)

        if not values[0] == 10: return False
        if not values[1] == 11: return False
        if not values[2] == 12: return False
        if not values[3] == 13: return False
        if not values[4] == 14: return False
        if self.flush() != True: return False
        return True

    def straightflush(self):
        if self.straight() != True: return False
        if self.flush() != True: return False
        return True

    def fours(self):
        pass

    def house(self):
        pass

    def flush(self):
        if len(set(self.suits)) != 1: return False
        return True

    def straight(self):
        values = list(set(self.values))
        values.sort()

        print(values)

        if not len(set(values)) == 5:
            return False
        if values[4] == 14:
            if not values[0] == 2 and not values[0] == 10: return False
            if not values[1] == 3 and not values[1] == 11: return False
            if not values[2] == 4 and not values[2] == 12: return False
            if not values[3] == 5 and not values[3] == 13: return False
        else:
            if not values[1] == values[0] + 1: return False
            if not values[2] == values[1] + 1: return False
            if not values[3] == values[2] + 1: return False
            if not values[4] == values[3] + 1: return False
        return True

    def threes(self):
        pass
        # for i in range(15):

    def pair(self):
        return 0

# deck = StandardDeck()
#
# deck.shuffle()
#
# cards = []
# cards.append(deck.deal())
# cards.append(deck.deal())
# cards.append(deck.deal())
# cards.append(deck.deal())
# cards.append(deck.deal())
#
# cards2 = []
# cards2.append(Card("Two", 10, "Hearts"))
# cards2.append(Card("Three", 11, "Hearts"))
# cards2.append(Card("Four", 12, "Hearts"))
# cards2.append(Card("Five", 13, "Hearts"))
# cards2.append(Card("Six", 14, "Hearts"))
#
# print(cards2)
#
# scorer = PokerScorer(cards2)
# print("Royal Flush: " + str(scorer.royal()))
# print("Straight Flush: " + str(scorer.straightflush()))
# print("Straight: " + str(scorer.straight()))
# print("Flush: " + str(scorer.flush()))
# # scorer.suits()
# # card = deck.deal()
# # card.showing = True
#
# # print(scorer)
# print(deck)