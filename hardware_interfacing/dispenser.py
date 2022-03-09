#Control for 6Shot dispensing mechanism 
#imports

#global constants
CAN_CAPACITY = 2000 #mL
MAX_DRINK_VOLUME = 341 # mL ~= 12oz, top line of a red solo cup

#CANISTER
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
        else:
            #<PHYSICAL DRAINING>
            # volume detection?
            self.current_volume -= n

    def info(self):
        print("\tINGREDIENT: " + self.ingredient_name)
        print("\tVOLUME: %.2f" % self.current_volume)

#DRINK
class drink:
    name = ''
    isAlcoholic = False
    volume = 0
    ingredients = []
    for i in range(6):
        ingredients.append(['NONE', 0]) # name, mL
    
    #  ALL TEMP INSTANCES?

    def __init__(self, namestr, alc:bool):
        self.isAlcoholic = alc
        self.name = namestr

    def addIngredient(self, ingstr, v):
        if (self.volume + v > MAX_DRINK_VOLUME):
            print('2000mL volume per drink would be exceeded')
            return False
        for i in range(len(self.ingredients)):
            if (self.ingredients[i] == ['NONE', 0]):
                self.ingredients[i] = [ingstr, v]
                self.volume += v
                return True
        print('6 ingredient maximum would be exceeded')
        return False

    def clearIngredient(self, ingName):
        for ing in self.ingredients:
            if (ing[0] == ingName):
                ing = ['NONE', 0]
                return True
        
        print('ingredient \'%s\' is not part of %s' % (ingName, self.name))
        return False

    def info(self):
        print("DRINK: %s" % (self.name))
        if (self.isAlcoholic):
            print("ALCOHOLIC")
        else:
            print("NON-ALCOHOLIC")
        print("INGREDIENTS: ")
        for i in range(len(self.ingredients)):
            ing = self.ingredients[i]
            if (ing != ['NONE', 0]):
                print("\t%s: %.2f" % (ing[0], ing[1]))
            # overfill warning?


    # def dispense(self, cyl:cylinder):
    #     for i in len(self.ingredients):
    #         cyl.dispense(i, self.ingredients[i])    

#CYLINDER
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
        if (self.spout != 5):
            self.spout += 1
        else: 
            self.spout = 0

    def rotate(self, n):
        for i in range(n):
            self.rotate()

    def dispense(self, d:drink, pos):
        if (self.spout != pos):
            while (self.spout != pos):
                self.rotate()
        for i in range(len(self.slot)):
            self.slot[i].drain(d[i])

# drink loading from database?
def loadDrink():
    # GET from database
    pass
