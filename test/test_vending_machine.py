#
# (c) Quality Without A Name 2011
#         Refactoring Course material
#
import unittest
from vending_machine import *
from chipknip import *

class VendingMachineTest(unittest.TestCase):
    def setUp(self):
        self.machine = VendingMachine()

    def test_choiceless_machine_delivers_nothing(self):
        self.assertEqual(Can.none, self.machine.deliver(Choice.cola))
        self.assertEqual(Can.none, self.machine.deliver(Choice.fanta))

    def test_delivers_can_of_choice(self):
        self.machine.configure(Choice.cola, Can.cola, 10)
        self.machine.configure(Choice.fanta, Can.fanta, 10)
        self.machine.configure(Choice.sprite, Can.sprite, 10)
        self.assertEqual(Can.cola, self.machine.deliver(Choice.cola))
        self.assertEqual(Can.fanta, self.machine.deliver(Choice.fanta))
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))

    def test_delivers_nothing_when_making_invalid_choice(self):
        self.machine.configure(Choice.cola, Can.cola, 10)
        self.machine.configure(Choice.fanta, Can.fanta, 10)
        self.machine.configure(Choice.sprite, Can.sprite, 10)
        self.assertEqual(Can.none, self.machine.deliver(Choice.beer))

    def test_delivers_nothing_when_not_paid(self):
        self.machine.configure(Choice.fanta, Can.fanta, 10, 2)
        self.machine.configure(Choice.sprite, Can.sprite, 10, 1)

        self.assertEqual(Can.none, self.machine.deliver(Choice.fanta))

    def test_delivers_fanta_when_paid(self):
        self.machine.configure(Choice.sprite, Can.sprite, 10, 1)
        self.machine.configure(Choice.fanta, Can.fanta, 10, 2)

        self.machine.set_value(2)
        self.assertEqual(Can.fanta, self.machine.deliver(Choice.fanta))
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))

    def test_delivers_sprite_when_paid(self):
        self.machine.configure(Choice.sprite, Can.sprite, 10, 1)
        self.machine.configure(Choice.fanta, Can.fanta, 10, 2)

        self.machine.set_value(2)
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))

    def test_add_payments(self):
        self.machine.configure(Choice.sprite, Can.sprite, 10, 1)
        self.machine.configure(Choice.fanta, Can.fanta, 10, 2)

        self.machine.set_value(1)
        self.machine.set_value(1)
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))

    def test_returns_change(self):
        self.machine.configure(Choice.sprite, Can.sprite, 10, 1)
        self.machine.set_value(2)
        self.assertEqual(2, self.machine.get_change())
        self.assertEqual(0, self.machine.get_change())


    def test_stock(self):
        self.machine.configure(Choice.sprite, Can.sprite, 1, 0)
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))

    def test_add_stock(self):
        self.machine.configure(Choice.sprite, Can.sprite, 1, 0)
        self.machine.configure(Choice.sprite, Can.sprite, 1, 0)
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))


    def test_checkout_chip_if_chipknip_inserted(self):
        self.machine.configure(Choice.sprite, Can.sprite, 1, 1)
        chip = Chipknip(10)
        self.machine.insert_chip(chip)
        self.assertEqual(Can.sprite, self.machine.deliver(Choice.sprite))
        self.assertEqual(9, chip.credits)

    def test_checkout_chip_empty(self):
        self.machine.configure(Choice.sprite, Can.sprite, 1, 1)
        chip = Chipknip(0)
        self.machine.insert_chip(chip)
        self.assertEqual(Can.none, self.machine.deliver(Choice.sprite))
        self.assertEqual(0, chip.credits)


