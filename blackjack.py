# Mini-project #6 - Blackjack 

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False # if player is still playing
outcome = ""
prompt = ""
score = 0
winner = 3 # 0: No winner yet, 1: Player wins, 2: Dealer wins - variable to keep track

#starting positon of player and dealer cards
player_pos = [50, 490]
dealer_pos = [50, 190]

holecard_pos = [dealer_pos[0] + CARD_SIZE[0] / 2, dealer_pos[1] + CARD_SIZE[1] / 2]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

#flag to see if deal is pressed within a game
is_deal = False

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, rotation):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE, rotation)
        
# define hand class

class Hand:
    def __init__(self):
        self.cards = [] #initialize to an empty list
        pass	# create Hand object

    def __str__(self):
        s = ""
        for card in self.cards:
            s += " " + str(card)
        return "Hand contains: " + s	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card) #appends card object to list cards
        pass	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand, see Blackjack video
        hand_value = 0
        aces = 0
        
        #for each card in the hand
        for card in self.cards:
            card_val = VALUES[card.get_rank()]
            hand_value += card_val
            
            #count aces in hand
            if card_val == 1:
                aces += 1
        
        if aces == 0:
            return hand_value
        else :
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    def draw(self, canvas, pos,rotation):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        space = 30
        for card in self.cards:
            card.draw(canvas, [pos[0] + (CARD_SIZE[0] + space) * i, pos[1]], rotation)
            i += 1
    


    
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(suit,rank) for suit in SUITS for rank in RANKS]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        return self.cards.pop()# deal a card object from the deck
    
    def __str__(self):
        s = ""
        for card in self.cards:
            s += str(card) + " "
        
        return "Deck : " + s# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, prompt, in_play, winner, deck, player_hand, dealer_hand, score, is_deal
    
    if not is_deal:
        #initialize objects
        deck  = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        #shuffle deck
        random.shuffle(deck.cards)

        #score
        if winner == 0:
            score -=1
        elif winner == 1:
            score += 1
        elif winner == 2:
            score -= 1

            
        is_deal = True # new game in progress
        winner = 0     # winner set to no one
        in_play = True # player is still choosing to hit or stand, hole card of dealer covered
        
        #deal two cards to dealer and player
        for i in range (2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
        
        outcome = ""
        prompt = "Hit or stand?"
        
    else: # handles the case where game has not ended but deal is pressed
        outcome = "Player loses! "
        prompt  = "New deal?"
        #winner is set to dealer
        winner = 2   
        
        #game has ended
        is_deal = False
    
def hit():
    global winner, in_play, outcome, prompt, is_deal
    
    if in_play and winner == 0:
        if player_hand.get_value() < 21: 
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "Player is busted, Dealer wins!"
            prompt = "New deal?"
        
            in_play = False
            winner = 2 #winner is dealer    
    
      
        is_deal = False
    
def stand():
    global winner, dealer_hand, outcome, prompt, in_play, is_deal
    
    playing = False
    in_play = False
    
    if winner == 0: # no winner yet 
        if player_hand.get_value() > 21:
            winner = 2 #winner is dealer
            outcome = "Player is busted, Dealer wins!"
            prompt = "New deal?"
                      
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
                
            if dealer_hand.get_value() > 21:
                outcome = "Dealer is busted, Player wins!"
                prompt = "New deal?"
                winner = 1 #winner is player
            else:
                if player_hand.get_value() <= dealer_hand.get_value():
                    outcome = "Dealer wins! New deal?"
                    prompt = "New deal?"

                    winner = 2 #winner is dealer  
                else:
                    outcome = "Player wins!"
                    prompt = "New deal?"
                    winner = 1 #winner is player
            

        is_deal = False

## draw handler    
def draw(canvas):
    
    #title and AJ cards
    
    show_card1 = Card("S", "A")
    show_card2 = Card("S", "J")
    show_card1.draw(canvas, [420, 30],60)
    show_card2.draw(canvas, [440, 30],120)
    
    canvas.draw_text("BLACKJACK", [50,80], 60, "Black") 
    canvas.draw_text("Score : " + str(score), [420,170], 30, "Beige") 
    
    
    #cards
    canvas.draw_text("DEALER", [dealer_pos[0],dealer_pos[1]-30], 30, "Black") 
    dealer_hand.draw(canvas,dealer_pos,0)
    
    canvas.draw_text("PLAYER", [player_pos[0],player_pos[1]-30], 30, "Black") 
    player_hand.draw(canvas, player_pos,0)
    
    #dealer hole card covered when player is still playing
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, holecard_pos, CARD_BACK_SIZE)
   
    
    #prompt and outcome
    canvas.draw_text(prompt,[10,player_pos[1]-90], 40, "MidnightBlue", "serif") 
    canvas.draw_text(outcome,[10,player_pos[1]-140], 40, "DeepPink", "serif") 


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
