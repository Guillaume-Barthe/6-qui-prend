
class Card():
    '''
    A Card object contains two attributes, self.value describes the value
    of the card. Self.cost descrbies the number of points a particular card is worth

    the repr method enables the print(card) command and tells the user the value
    of a particular card
     '''

    def __init__(self,value):
        self.value = value
        lastdigit = int(str(value)[-1])
        if value == 55:
            self.cost = 7    #PARTICULAR 55 Card
        elif value%11 == 0:
            self.cost = 5
        elif lastdigit == 5:
            self.cost = 2
        elif lastdigit == 0:
            self.cost = 3
        else:
            self.cost = 1

    def __repr__(self):

        return "This card has value "+str(self.value)+" and costs "+str(self.cost)+" points "
