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
score = 0
winner = 3 # 0: No winner yet, 1: Player wins, 2: Dealer wins - variable to keep track

#starting positon of player and dealer cards
player_pos = [50, 400]
dealer_pos = [50, 200]

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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
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
            
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + CARD_SIZE[0] * i, pos[1]])
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
    global outcome, in_play, winner, deck, player_hand, dealer_hand, score, is_deal
    
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
            outcome = "Player lose"
            winner = 3

        elif winner == 1:
            score += 1
        elif winner == 2:
            score -= 1

        is_deal = True
        winner = 0
        in_play = True
        #deal two cards to dealer and player
        for i in range (2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())


        ####################printing hands to console ###########################################
        print "			-- New game --"
        print "Current score : ",score
        print "player hand: " + str(player_hand) + " val: " + str(player_hand.get_value())
        print "dealer hand: " + str(dealer_hand) + " val: " + str(dealer_hand.get_value())  
        print
        outcome = "Hit or stand?"
    else:
        outcome = "Player loses"
        winner = 2
        is_deal = False
    
def hit():
    global winner, in_play, outcome, is_deal
    
    if in_play and winner == 0:
        if player_hand.get_value() < 21: #made just less than not equal?
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            print "Player is busted!"
            print "Dealer wins!"
            outcome = "New Deal"
            
            
           
            in_play = False
            winner = 2 #winner is dealer
            outcome = "New Deal"
    
    
        ############CONSOLE######################
        print "player hand: " + str(player_hand) + " val: " + str(player_hand.get_value())
        print "dealer hand: " + str(dealer_hand) + " val: " + str(dealer_hand.get_value())  
        print
        ############CONSOLE######################
        is_deal = False
    
def stand():
    global winner, dealer_hand, outcome, in_play, is_deal
    playing = False
    in_play = False
    if winner == 0: # no winner yet 
        if player_hand.get_value() > 21:
            print "Player is busted!"
            print "Dealer wins!"
           
            winner = 2 #winner is dealer
            
            outcome = "New Deal"
           
            
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
                
            if dealer_hand.get_value() > 21:
                print "Dealer is busted!"
                print "Player wins!"
                winner = 1 #winner is player
            else:
                if player_hand.get_value() <= dealer_hand.get_value():
                    print "Dealer wins!"
                    winner = 2 #winner is dealer  
                else:
                    print "Player wins!"
                    winner = 1 #winner is player
            outcome = "new deal"
            
        
        ############CONSOLE######################
        print "player hand: " + str(player_hand) + " val: " + str(player_hand.get_value())
        print "dealer hand: " + str(dealer_hand) + " val: " + str(dealer_hand.get_value())  
        print
        ############CONSOLE######################
        is_deal = False

## draw handler    
def draw(canvas):
    
    #title
    
    canvas.draw_text("BLACKJACK", [70,70], 80, "Black") 
    canvas.draw_text("Score : " + str(score), [400,120], 30, "Blue")      
    canvas.draw_text("TEST : " + str(winner), [400,150], 30, "Blue")      

    
    #cards
    canvas.draw_text("DEALER", [dealer_pos[0],dealer_pos[1]-20], 30, "Black") 
    dealer_hand.draw(canvas,dealer_pos)
    
    canvas.draw_text("PLAYER", [player_pos[0],player_pos[1]-20], 30, "Black") 
    player_hand.draw(canvas, player_pos)
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, holecard_pos, CARD_BACK_SIZE)
   
    
    #outcome
    
    canvas.draw_text(outcome,[player_pos[0]+250,player_pos[1]-20], 40, "AQUA", "serif") 
    


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
