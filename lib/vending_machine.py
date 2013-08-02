#
# (c) Quality Without A Name 2011
#         Refactoring Course material
#
from enums import *
from can_container import *

class VendingMachine:
    def __init__(self):
        self.cans = {}
        self.payment_method = None

    def set_value(self, v):
        self.payment_method = 1
        if hasattr(self,'c'):
            self.c += v
        else:
            self.c = v

    def insert_chip(self, chipknip):
        # TODO
        # can't pay with chip in brittain
        self.payment_method = 2
        self.chipknip = chipknip

    # delivers the can if all ok
    def deliver(self, choice):
        res = None
        #
        #step 1: check if choice exists
        #
        if self.cans.has_key(choice):
            #
            # step2 : check price
            #
            if self.cans[choice].price == 0 :
                res = self.cans[choice].type
            # or price matches
            else:
                if self.payment_method == 1: # paying with coins
                    if self.c != None and self.cans[choice].price <= self.c:
                        res = self.cans[choice].type
                        self.c -= self.cans[choice].price

                elif self.payment_method == 2: # paying with chipknip - 
                    # TODO: if this machine is in belgium this must be an error
                    if (self.chipknip.has_value(self.cans[choice].price)):
                        self.chipknip.reduce(self.cans[choice].price)
                        res = self.cans[choice].type

                else:
                    # TODO: Is this a valid situation?:
                    #  larry forgot the else: clause 
                    #  i added it, but i am acutally not sure as to wether this is a problem
                    #  unknown payment
                    pass # i think(i) nobody inserted anything
        else:
            res = Can.none
        #
        # step 3: check stock
        #
        if (res and res != Can.none):
            if (self.cans[choice].amount <= 0):
                res = Can.none
            else:
                self.cans[choice].amount -= 1
        #
        # if can is set then return
        # otherwise we need to return the none
        if (res is None):
            return Can.none
        return res

    def get_change(self):
        to_return = 0
        if (self.c > 0):
            to_return = self.c
            self.c = 0
        return to_return

    def configure(self, choice, c, n, price = 0):
        self.price = price
        if (self.cans.has_key(choice)):
            self.cans[choice].amount += n
            return

        can = CanContainer()
        can.type = c
        can.amount = n
        can.price = price
        self.cans[choice] = can
