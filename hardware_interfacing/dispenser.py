# Control for 6Shot dispensing mechanism 

#imports
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
sys.path.append('../web-app')
# from global_var import DrinkInfo, EmployeeInfo, IngredientInfo
from database import *
from flask_sqlalchemy import SQLAlchemy


#global constants
CAN_CAPACITY = 2000 #mL
MAX_DRINK_VOLUME = 341 # mL ~= 12oz, top line of a red solo cup
EMPTY_INGREDIENT = ['NONE', 0 , 0] # name, mL, alc %

# local vars
# drinkQueue = []

# CANISTER
class can:
    ingredient_name = 'EMPTY'
    current_volume = 0

    def __init__(self, ingr_name='EMPTY', vol=0):
        self.ingredient_name = ingr_name
        self.current_volume = vol

    def edit(self, ingr_name, vol):
        self.ingredient_name = ingr_name
        self.current_volume = vol

    def drain(self, n):
        if (n > self.current_volume):
            print('INSUFFICIENT CAN VOLUME (%.2f)' % n)
            return False
        else:
            #<PHYSICAL DRAINING>
            # volume detection?
            print('%.2f - %.2f' % (self.current_volume, n))
            self.current_volume -= n
            print('= %.2f' % self.current_volume)
            return True

    def info(self):
        print("\tINGREDIENT: " + self.ingredient_name)
        if (self.ingredient_name != 'EMPTY'):
            print("\tVOLUME: %.2f" % self.current_volume)
# END OF CANISTER

# DRINK
class drink:
    name = ''
    alcohol_content = 0 #alcohol content by %, between 0-1
    volume = 0
    ingredients = []
    for i in range(6):
        ingredients.append(EMPTY_INGREDIENT) # name, mL, alc %

    def __init__(self, namestr = ''):
        self.name = namestr

    def addIngredient(self, ingstr, v, a=0.00):
        if (self.volume + v > MAX_DRINK_VOLUME):
            print('2000mL volume per drink would be exceeded')
            return False
        if (0 > a or a > 1):
            print('NON-PERCENTAGE ALCOHOL CONTENT FOR')
            return False
        for i in range(len(self.ingredients)):
            if (self.ingredients[i] == EMPTY_INGREDIENT):
                self.ingredients[i] = [ingstr, v, a]
                self.update()
                return True
        print('6 ingredient maximum would be exceeded')
        return False

    def clearIngredient(self, ingName):
        for i in range(len(self.ingredients)):
            if (self.ingredients[i][0] == ingName):
                self.ingredients[i] = EMPTY_INGREDIENT
                self.update()
                return True
        print('ingredient \'%s\' is not part of %s' % (ingName, self.name))
        return False

    def update(self):
        # print('updating')
        self.volume = 0
        alc_total = 0
        for ing in self.ingredients:
            self.volume += ing[1]
            alc_total += ing[1] * ing[2] # vol * %
        self.alcohol_content = alc_total / self.volume

    def info(self):
        print("DRINK: %s %0.2fmL" % (self.name, self.volume))
        if (self.alcohol_content > 0):
            p = self.alcohol_content * 100
            print("ALCOHOLIC (%.2f%%)" % p) #  bruh why isn't % an escape character
        else:
            print("NON-ALCOHOLIC")
        print("INGREDIENTS: ")
        for i in range(len(self.ingredients)):
            ing = self.ingredients[i]
            if (ing != EMPTY_INGREDIENT):
                print("\t%s: %.2fmL" % (ing[0], ing[1]))
# END OF DRINK

# CYLINDER
class cylinder:
    can1 = can()
    can2 = can()
    can3 = can()
    can4 = can()
    can5 = can()
    can6 = can()
    slot = [can1, can2, can3, can4, can5, can6]
    spout = 0 # current can; adjust to detect?

    def __init__(self):
        pass

    def info(self):
        for i in range(len(self.slot)):
            isSpoutStr = ''
            if (self.spout == i):
                isSpoutStr = "(current spout)"
            print("CAN %d: %s" % (i+1, isSpoutStr))
            self.slot[i].info()

    def editCan(self, pos, ingr_name, vol):
        self.slot[pos-1].edit(ingr_name, vol)

    def rotate(self):
        #<PHYSICAL ROTATING>
        print('%d -> %d' % (self.spout, (self.spout + 1) % 6))
        self.spout = (self.spout + 1) % 6 

    def rotateN(self, n):
        for i in range(n):
            self.rotate()

    def dispense(self, vol, pos):
        if (self.spout != pos):
            while (self.spout != pos):
                self.rotate()
        if not self.slot[pos].drain(vol):
            print('DISPENSING FAILED')
            return False
        return True

    def checkDrink(self, d:drink):
        # valid drink check
        drink_ing = set()
        cylinder_ing = set()
        print("VALIDATING:")
        for i in range(6):
            if (d.ingredients[i] != EMPTY_INGREDIENT):
                drink_ing.add(d.ingredients[i][0])
        # print(drink_ing)
        for s in self.slot:
            cylinder_ing.add(s.ingredient_name)
        # print(cylinder_ing)
        if not (drink_ing.issubset(cylinder_ing)):
            print("\tINGREDIENTS FOR <%s> ARE NOT LOADED" % d.name)
            return False
        # quantity check
        for ing in d.ingredients:
            for jng in self.slot:
                if (jng.ingredient_name == ing[0]):
                    print(jng.ingredient_name + ':')
                    print("\tCURRENT\tNEEDED")
                    print("\t%.2f\t%.2f\tmL" % (jng.current_volume, ing[1]))
                    if (jng.current_volume < ing[1]):
                        print("INSUFFICIENT <%s> VOLUME" % ing[0])
                        return False
                    else:
                        continue
        print("DRINK CAN BE MADE")
        return True
    
    def makeDrink(self, d:drink):
        if not (self.checkDrink(d)):
            print('DRINK CREATION FAILED')
            return False
        for c in self.slot:
            for i in d.ingredients:
                if (c.ingredient_name==i[0]):
                    # c.drain(i[1])
                    v = i[1]
                    p = self.slot.index(c)
                    self.dispense(v, p)
                    continue
        # for ing in d.ingredients:
        #     self.dispense(ing[1], )
# END OF CYLINDER

# DATABASE INTERFACING
# drink loading
def loadDrink(drinkID):
    db_drink = Drinks.query.filter_by(id = drinkID).first()
    dr = drink(str(db_drink.name))
    # print(db_drink.bev2)
    # print(str(db_drink.bev2 != "None"))
    if (str(db_drink.bev1) != "None"):
        ingredient1 = Ingredients.query.filter_by(name = db_drink.bev1).first()
        dr.addIngredient(
            str(db_drink.bev1),
            float(db_drink.vol1),
            float(ingredient1.alcohol))
    if (str(db_drink.bev2) != "None"):
        ingredient2 = Ingredients.query.filter_by(name = db_drink.bev2).first()
        dr.addIngredient(
            str(db_drink.bev2),
            float(db_drink.vol2),
            float(ingredient2.alcohol))
    if (str(db_drink.bev3) != "None"):
        ingredient3 = Ingredients.query.filter_by(name = db_drink.bev3).first()
        dr.addIngredient(
            str(db_drink.bev3),
            float(db_drink.vol3),
            float(ingredient3.alcohol))
    if (str(db_drink.bev4) != "None"):
        ingredient4 = Ingredients.query.filter_by(name = db_drink.bev4).first()
        dr.addIngredient(
            str(db_drink.bev4),
            float(db_drink.vol4),
            float(ingredient4.alcohol))
    if (str(db_drink.bev5) != "None"):
        ingredient5 = Ingredients.query.filter_by(name = db_drink.bev5).first()
        dr.addIngredient(
            str(db_drink.bev5),
            float(db_drink.vol5),
            float(ingredient5.alcohol))
    if (str(db_drink.bev6) != "None"):
        ingredient6 = Ingredients.query.filter_by(name = db_drink.bev6).first()
        dr.addIngredient(
            str(db_drink.bev6),
            float(db_drink.vol6),
            float(ingredient6.alcohol))

    return dr
    
def makeOrder(cyl:cylinder):
    order = Orders.query.first()
    print(order.drink_id)
    dr = loadDrink(order.drink_id)
    dr.info()
    cyl.makeDrink(dr)
    cyl.info()
    # update slot database entry
    for i in range(6):
        slot = Slots.query.filter_by(slot = i+1).first()
        # print(float(slot.volume))
        # print(float(cyl.slot[i].current_volume))
        if (float(slot.volume) != float(cyl.slot[i].current_volume)):
            slot.volume = cyl.slot[i].current_volume
            db.session.commit()
        if (i != cyl.spout):
            # print('n')
            slot.is_current_spout = 0
        else:
            slot.is_current_spout = 1
    # pop queue
    db.session.delete(order)
    db.session.commit()

# dispenser contents loading
def loadCylinder():
    cyl = cylinder()
    for s in Slots.query.all():
        # print(s.ingredient_id)
        if (str(s.ingredient_id) != "None"):
            ing_pos = s.slot
            # print(ing_pos)
            ing = Ingredients.query.filter_by(id = s.ingredient_id).first()
            ing_name = str(ing.name)
            # print(ing_name)
            ing_vol = float(s.volume)
            # print(ing_vol)
            cyl.editCan(ing_pos, ing_name, ing_vol)
    print('CYLINDER DATA LOADED')
    cyl.info()
    return cyl

def queueDrink(sequence:str):
    # PUSH SEQEUNCE TO POSTGRES TABLE
    pass


