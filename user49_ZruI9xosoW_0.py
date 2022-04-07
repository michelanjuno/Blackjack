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
in_play = False
outcome = ""
score = 0

player_message = ""


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        
# define hand class. Need to check the get_value method and the draw method. 
class Hand:
    def __init__(self):
        self.field = []

    def __str__(self):
        ans = "Hand contains"
        for i in range(len(self.field)):
            ans += " " + self.field[i].suit + self.field[i].rank
        return ans  

    def add_card(self, card):
        self.field.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = []
        sum = 0
               
        for c in self.field:
            hand_value.append(c.get_rank())
            
        for i in range(len(hand_value)):
            sum += VALUES[hand_value[i]]
            
        if 'A' in hand_value:
            if sum <= 11: 
                return sum + 10
        return sum      
                       
            
   
    def draw(self, canvas, pos):

        for c in self.field:
#            if self.field.index(c) = 0:
#                c.draw(canva
            c.draw(canvas, [self.field.index(c)*CARD_SIZE[0]+ pos[0], pos[1]])
        
# define deck class. Checked with the test cases.  
class Deck:
    def __init__(self):
    # create a Deck object
        self.deck_list = []
        for s in SUITS:
            for r in RANKS:
                self.deck_list.append(Card(s,r))
           
    def shuffle(self):
    # shuffle the deck 
        random.shuffle(self.deck_list)
        return self.deck_list

    def deal_card(self):
        card = random.choice(self.deck_list)
        self.deck_list.remove(card)
        return card

    def __str__(self):
    # return a string representing the deck
        ans = "Deck contains"
        for i in range(len(self.deck_list)):
            ans += " " + self.deck_list[i].suit + self.deck_list[i].rank
        return ans  



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, dealer_first_card, player_message, my_deck, score
    
    player_hand = Hand()
    dealer_hand = Hand()
    my_deck = Deck()
    # your code goes here
    if (not in_play):
        
        my_deck.shuffle()
        in_play = True
        score = 0
        outcome = ""
    
        #deal cards from the DECK, and add the dealt cards to player's and deal's hand respectively.
        player_hand.add_card(my_deck.deal_card())
        player_hand.add_card(my_deck.deal_card())
        dealer_first_card = my_deck.deal_card()
        dealer_hand.add_card(dealer_first_card)
        dealer_hand.add_card(my_deck.deal_card())
        player_message = "Hit or stand?" 
    else:   
        outcome = "You gave up."
        score -= 1 
        my_deck = Deck()
        my_deck.shuffle()
        player_message = "New deal?"
        in_play = False
        

def hit():
    global in_play, player_hand, player_message, outcome, score 
    
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(my_deck.deal_card())    
        
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21: 
        in_play = False
        score -= 1 
        outcome = "R.I.P."
        player_message = "New deal?"
    
def stand():
    global in_play, dealer_hand, player_hand, outcome, score, player_message, my_deck
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
#            if dealer_hand.get_value() > 21:
#                outcome = "You win!"
#                score += 1
#       
#            else:
#                if player_hand.get_value() > dealer_hand.get_value():
#                    outcome = "You win!"
#                    score += 1 
#                else: 
#                    outcome = "R.I.P."
#                    score -= 1 
#            in_play = False
#            player_message = "New deal?"
    else:
        return outcome
    
    # assign a message to outcome, update in_play and score   
    if dealer_hand.get_value() > 21:
        outcome = "You win!"
        score += 1
       
    else:
        if player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win!"
            score += 1 
        else: 
            outcome = "R.I.P."
            score -= 1 
    in_play = False
    player_message = "New deal?"


# draw handler. NEED TO FIGURE OUT HOW TO DRAW THE HOLE CARD. check the card_back image, only containing 2 back images.     
def draw(canvas):
    global dealer_first_card, player_hand, dealer_hand, dealer_first_card_loc

    
    dealer_hand.draw(canvas, [50, 200])
    player_hand.draw(canvas, [50, 400])
    if in_play:
        #Dealer's first card is facing down when in play.
        dealer_first_card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]) 
                                
        canvas.draw_image(card_back, dealer_first_card_loc, CARD_BACK_SIZE, [50+ CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
        
    else:
        #reveal dealer's hole card at the end of each round. 
        canvas.draw_image(card_images, dealer_first_card_loc, CARD_SIZE, [50 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)
    
    #print out messages for the player.
    canvas.draw_text(outcome, [300, 150], 20, "White") 
    #display the player's score throughout the game play. 
    canvas.draw_text("Score = " + str(score), [400,100],30, "White")
    #display the BLACKJACK title
    canvas.draw_text("BLACKJACK", [50,50], 50, "Black")
    #display the player message
    canvas.draw_text(player_message, [300,350], 20, "White")
    #display titles for player's hand and dealer's hand respectively.
    canvas.draw_text("Dealer's hand", [50, 150], 20, "Black")
    canvas.draw_text("Player's hand", [50, 350], 20, "Black")
    
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
print in_play

# remember to review the gradic rubric