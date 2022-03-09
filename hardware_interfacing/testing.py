from dispenser import *

#TEST FUNCTIONS
def infotest():
    testCylinder = cylinder()
    testCylinder.editCan(0, "stoli_vodka", 750)
    testCylinder.editCan(1, "wildTurkey_bourbon", 750)
    testCylinder.editCan(2, "coca_cola", 2000)
    testCylinder.info()

def drinktest():
    # testDrink = drink('test', False)
    testDrink = drink('whiskey&coke', True)
    testDrink.addIngredient("wildTurkey_bourbon", 100)
    testDrink.addIngredient("coca_cola", 100)
    testDrink.info()
    testDrink.clearIngredient("test")

def waterTest():
    water = drink('glassOfWater', False)
    # water.addIngredient('water', 341)
    # water.addIngredient('water2', 1)
    for i in range(7):
        s = ('water' + str(i+1))
        water.addIngredient(s,10)
    water.info()

#MAIN
def main():
    # infotest()
    # drinktest()
    waterTest()
    
main()