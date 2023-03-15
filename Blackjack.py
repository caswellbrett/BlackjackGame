# libraries
from random import seed
from random import shuffle
from tkinter import *

seed()

# Data Structure
# Assume a deck of cards index from 0 to 51
# 0 - 12    A 2 3 4 5 6 7 8 9 10 J Q K hearts♥
# 13 - 25   A to K diamonds♦
# 26 - 38   A to K clubs♣
# 39 - 51   A to K spades♠

deck = list(range(52)) # [0, 1, 2, 3, ..., 51]
#deck = [0, 10, 5] remove for testing

cardInd = [] # card index drawn from deck
cardDsp = [] # card display (rank and suit)
cardVal = [] # numeric value of card's rank (ex. A = 1)

dCardDsp = []
dCardVal = []
dCardTDsp = []
dCardInd = []

bet = 10
ace = 0
ace2 = 0
played = True

# functions
def cardDisplay(card):
    # converts card index to the card dislay (ex. 16 -> '4D')
    suit = ""
    if(card >= 0 and card <= 12):
        suit = "♥"
    elif(card >= 13 and card <= 25):
        suit = "♦"
    elif(card >= 26 and card <= 38):
        suit = "♣"
    elif(card >= 39 and card <= 51):
        suit = "♠"
    rank = str(card % 13 + 1)
    if(rank == "1"):
        rank = "A"
    if(rank == "11"):
        rank = "J"
    if (rank == "12"):
        rank = "Q"
    if (rank == "13"):
        rank = "K"
    cardDspReturn = rank + suit
    return cardDspReturn

def deal():
    global ace
    global played
    played = True
    card = deck.pop(0) # draw a card from top of deck
    cardInd.append(card) # add card to index
    cardDsp.append(cardDisplay(card))
    if (cardDisplay(card)[0] == "A"):
        ace += 1
    cardVal.append(min(card % 13 + 1, 10))
    print(cardDsp)
    print(sum(cardVal), cardVal)
    playerHand.set("    ".join(cardDsp))
    playerValue = counting(cardVal)
    if (playerValue >= 21 or len(cardVal) == 5):
        stay()

def stay():
    global ace2
    global played
    played = False
    oCardVal = counting(dCardVal)
    if (len(dCardDsp) < 2):
        dCard = deck.pop(0)
        dCardInd.append(dCard)
        dCardTDsp.append(cardDisplay(dCard))
        if (cardDisplay(dCard)[0] == "A"):
            ace2 += 1
        if (len(dCardDsp) == 0):
            dCardDsp.append("✗")
        else:
            dCardDsp.append(cardDisplay(dCard))
        dCardVal.append(min(dCard % 13 + 1, 10))
        dealersHand.set("   ".join(dCardDsp))
    else:
        while (oCardVal < 17):
            oCardVal = counting(dCardVal)
            if (oCardVal < 17):
                dCard = deck.pop(0)
                dCardInd.append(dCard)
                dCardTDsp.append(cardDisplay(dCard))
                if (cardDisplay(dCard)[0] == "A"):
                    ace2 += 1
                dCardDsp.append(cardDisplay(dCard))
                dCardVal.append(min(dCard % 13 + 1, 10))
                dealersHand.set("   ".join(dCardDsp))
            else:
                break
        winOrLose()

def betting():
    global bet
    userBet = betEntry.get()
    try:
        if (float(userBet) <= 10 or float(userBet) >= 1000):
            errBetMsg.set("Please keep bets between $10 and $1000.")
        else:
            bet = round(float(userBet), 2)
            errBetMsg.set("Bet placed: $" + userBet)
    except:
        errBetMsg.set("Please only place numbers in the betting box.")
    reset()

def counting(cardList):
    global ace
    global ace2
    global played
    value = sum(cardList)
    if (played == True):
        for i in range(ace):
            value += 10
            if (value > 21):
                value -= 10
    if (played == False):
        for i in range(ace2):
            value += 10
            if (value > 21):
                value -= 10
    return value

def reset():
    global ace
    global ace2
    # reshuffle deck of cards
    deck.extend(cardInd) # place drawn cards back
    deck.extend(dCardInd)
#    shuffle(deck)
    del cardInd[:]
    del cardVal[:]
    del cardDsp[:]
    del dCardVal[:]
    del dCardDsp[:]
    del dCardTDsp[:]
    playerHand.set("")
    dealersHand.set("")
    pVal.set("")
    dVal.set("")
    winOrLoseStr.set("")
    ace = 0
    ace2 = 0
    for i in range(2):
        deal()
        stay()

def winOrLose():
    global played
    played = True
    playerValue = counting(cardVal)
    played = False
    dealerValue = counting(dCardVal)
    blackjack = False
    push = False
    win = False
    lose = False
    dealersHand.set("   ".join(dCardTDsp))
    pVal.set("Player's card value: " + str(playerValue))
    dVal.set("Dealer's card value: " + str(dealerValue))
    if (len(cardVal) == 2 and playerValue == 21):
        blackjack = True
        if (len(dCardVal) == 2 and dealerValue == 21):
            blackjack = False
            push = True
    elif (len(dCardDsp) == 2 and dealerValue == 21):
        lose = True
    elif (playerValue > 21):
        lose = True
    elif (dealerValue > 21):
        win = True
    elif (playerValue <= 21 and dealerValue <= 21):
        if (len(cardVal) == 5):
            win = True
        elif(playerValue > dealerValue):
            win = True
        elif(playerValue < dealerValue):
            lose = True
        elif(playerValue == dealerValue):
            push = True
    if (push == True):
        winOrLoseStr.set("Push!  Your bet of $" + str(bet) + " is returned.")
    if (win == True):
        winOrLoseStr.set("Win!  You won $" + str(bet) + "!")
    if (lose == True):
        winOrLoseStr.set("Lose.  You lost $" + str(bet) + ".")
    if (blackjack == True):
        winOrLoseStr.set("Blackjack! You won $" + str(round(bet * (3/2))) + ".")


# Graphical user interface

root = Tk()

root.geometry("500x500")
root.title("Blackjack!")


playerHand = StringVar()
playerHand.set("")

dealersHand = StringVar()
dealersHand.set("")

errBetMsg = StringVar()
errBetMsg.set("")

winOrLoseStr = StringVar()
winOrLoseStr.set("")

pVal = StringVar()
pVal.set("")

dVal = StringVar()
dVal.set("")

handDspLbl = Label(root, textvariable = playerHand)
handDspLbl.grid(row = 0, column = 0)

handLbl = Label(root, text = "Player's Hand: ")
handLbl.grid(row = 1, column = 0)

dealersHandL = Label(root, textvariable = dealersHand)
dealersHandL.grid(row = 2, column = 0)

dealerLbl = Label(root, text = "Dealer's Hand")
dealerLbl.grid(row = 3, column = 0)

dealBtn = Button(root, text = "deal/hit", command = deal)
dealBtn.grid(row = 4, column = 0)

stayBtn = Button(root, text = "stay/stand", command = stay)
stayBtn.grid(row = 5, column = 0)

shuffleBtn = Button(root, text = "reset/shuffle", command = reset)
shuffleBtn.grid(row = 6, column = 0)

betLbl = Label(root, text = "Enter bet here:")
betLbl.grid(row = 8, column = 0)

betEntry = Entry(root, width = 5)
betEntry.grid(row = 9, column = 0)

betBtn = Button(root, text = "Place bet", command = betting)
betBtn.grid(row = 10, column = 0)

errBetLbl = Label(root, textvariable = errBetMsg, fg = "red")
errBetLbl.grid(row = 10, column = 1)

pValLbl = Label(root, textvariable = pVal)
pValLbl.grid(row = 12, column = 0)

dValLbl = Label(root, textvariable = dVal)
dValLbl.grid(row = 13, column = 0)

winOrLoseLbl = Label(root, textvariable = winOrLoseStr)
winOrLoseLbl.grid(row = 16, column = 0)

# Actions:

root.mainloop()

'''
Rules for Blackjack!
1.  First card is dealt to player, then to dealer,
    back to player, and finally to dealer.

2.  Only dealer's second card faces up. Player's cards
    are both faced up.

3.  a) Player wins if their total value is larger than the
    dealer's total WITHOUT GOING ABOVE 21.

    b) Player automatically loses if they go over 21
    (i.e. bust).

    c) Player and dealer tie (i.e. push) if they have
    the same total without bust.

4.  Player can choose to hit (i.e. receive a card)
    or stay (no cards). Aces count as either 1 or 11.
    Face cards have a value of 10.

5.  a) Player wins automatically if they get blackjack (unless
    the dealer also gets blackjack resulting in a push).
    
    b) Dealer wins with blackjack automatically over player's
    five card Charlie or 21 (unless player has blackjack
    which results in a push).

6.  After player stays (i.e. no more cards), dealer
    must take a card if the total is 16 or under; stay
    if 17 or over.
   
Future considerations:
1. Create two hands: one for player and one for dealer.
2. Create a new variable for dealer's hidden card.
3. Deal to dealer first by deck.pop(1) and deck.pop(2),
   where deck.pop(1) is the hidden card and deck.pop(2)
   goes into dealer's visible hand.
4. Deal the next two cards to player.

'''
