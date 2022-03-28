#Control for 6Shot dispensing mechanism 
#imports
from global_var import DrinkInfo, EmployeeInfo, IngredientInfo
from database import db, Employees, Users, Credentials, Drinks, Ingredients

#global constants
CAN_CAPACITY = 2000 #mL
MAX_DRINK_VOLUME = 341 # mL ~= 12oz, top line of a red solo cup
EMPTY_INGREDIENT = ['NONE', 0 , 0]

# local vars
drinkQueue = []

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
            print('INSUFFICIENT CAN VOLUME\n')
            return False
        else:
            #<PHYSICAL DRAINING>
            # volume detection?
            self.current_volume -= n
            return True

    def info(self):
        print("\tINGREDIENT: " + self.ingredient_name)
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
    
    #  ALL TEMP INSTANCES?

    def __init__(self, namestr):
        self.name = namestr

    def addIngredient(self, ingstr, v, a=0):
        if (self.volume + v > MAX_DRINK_VOLUME):
            print('2000mL volume per drink would be exceeded')
            return False
        if (0 > a or a > 1):
            print('non-percentage alcohol content')
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
        self.slot[pos].edit(ingr_name, vol)

    def rotate(self):
        #<PHYSICAL ROTATING>
        self.spout = (self.spout + 1) % 6 

    def rotate(self, n):
        for i in range(n):
            self.rotate()

    def dispense(self, vol, pos):
        if (self.spout != pos):
            while (self.spout != pos):
                self.rotate()
        for i in range(len(self.slot)):
            self.slot[i].drain(vol)

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
    
    def makeDrink(self, d:drink):
        self.checkDrink(d)
        #pull from queue
# END OF CYLINDER


# drink loading from database?
def loadDrink(drinkID):
    # GET from database
    db_drink = Drinks.query.filter_by(id = drinkID).first()
    dname = db_drink.name
    dr = drink(dname)

    if not (db_drink.bev1.name != ''): #?
        ing = []
        ing.append[db_drink.bev1.name]
        ing.append[db_drink.vol1] #?
        # ing.append[db_drink.]
        
    

    # return dr
    pass
