class player:
    '''
    A player object describes the player and his hand. The player can either be a is_machine
    or a human and has a hand from 10 to 0 cards.

    The repr method enables the print(player) command and tells the user the values
    of each card in his hand
     '''

    def __init__(self, is_machine):
        self.size_hand = 10
        self.hand = []
        self.is_machine = is_machine
