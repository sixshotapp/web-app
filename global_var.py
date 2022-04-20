class EmployeeInfo:
    first_name = ""
    last_name = ""
    email = ""

class IngredientInfo:
    id = 0
    name = ""
    available = 0
    pump = 0
    alcohol = 0

class DrinkInfo:
    id = 0
    name = ""
    price = 0
    bev1 = ""
    vol1 = ""
    bev2 = ""
    vol2 = ""
    bev3 = ""
    vol3 = ""
    bev4 = ""
    vol4 = ""
    bev5 = ""
    vol5 = ""
    bev6 = ""
    vol6 = ""

MAX_DRINK_VOLUME = 341

class drink:

    def __init__(self, name, alcohol_content=0, volume=0, ingredients=[]):
        self.name=name
        self.alcohol_content = alcohol_content
        self.volume = volume
        self.ingredients = ingredients
        for i in range(6):
            ingredients.append(['NONE', 0 , 0]) # name, mL, alc %

    def clear(self):
        self.__init__(name='')

    def addIngredient(self, ingstr, v, a=0.00):
        if (self.volume + v > MAX_DRINK_VOLUME):
            print('341mL volume per drink would be exceeded')
            return False
        if (0 > a or a > 1):
            print('NON-PERCENTAGE ALCOHOL CONTENT FOR')
            return False
        for i in range(len(self.ingredients)):
            if (self.ingredients[i] == ['NONE', 0 , 0]):
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
            if (ing != ['NONE', 0 , 0]):
                print("\t%s: %.2fmL" % (ing[0], ing[1]))
