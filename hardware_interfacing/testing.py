from dispenser import *
from time import sleep

#TEST FUNCTIONS
def infotest():
    testCylinder = cylinder()
    testCylinder.editCan(0, "stoli_vodka", 750)
    testCylinder.editCan(1, "wildTurkey_bourbon", 750)
    testCylinder.editCan(2, "coca_cola", 2000)
    testCylinder.info()

def drinktest():
    # testDrink = drink('test', False)
    testDrink = drink('whiskey&coke')
    testDrink.addIngredient("wildTurkey_bourbon", 20, 0.4)
    testDrink.addIngredient("coca_cola", 80)
    testDrink.info()
    # sleep(1)
    # testDrink.clearIngredient("test")
    # sleep(1)
    # testDrink.clearIngredient("wildTurkey_bourbon")
    # testDrink.clearIngredient("coca_cola")
    # testDrink.info()

def waterTest():
    water = drink('glassOfWater', False)
    # water.addIngredient('water', 341)
    # water.addIngredient('water2', 1)
    for i in range(7):
        s = ('water' + str(i+1))
        water.addIngredient(s,10)
    water.info()

def dispenseTest():
    testCylinder = cylinder()
    testCylinder.editCan(0, "stoli_vodka", 750)
    testCylinder.editCan(1, "wildTurkey_bourbon", 750)
    testCylinder.editCan(2, "coca_cola", 2000)
    testCylinder.info()
    print('-'*20)
    
    testDrink = drink('whiskey&coke')
    testDrink.addIngredient("wildTurkey_bourbon", 20, 0.4)
    testDrink.addIngredient("coca_cola", 80)
    # testDrink.addIngredient("stuff", 10)

    testCylinder.makeDrink(testDrink)
    testCylinder.info()

def qTest():
    drinkQueue.append('ur mom')
    print(drinkQueue)

def loadTest():
    testDrink = loadDrink(2)
    testDrink.info()

def dbTest():
    # testDrink = loadDrink(2)
    # testDrink.info()

    testcyl = loadCylinder()
    # add_order = Orders(user_id = 1, drink_id = 2)
    # db.session.add(add_order)
    # db.session.commit()
    makeOrder(testcyl)

def postest():
    # a = ['w', 'x', 'y', 'z']
    # print(a.index('x'))
    testCylinder = cylinder()
    testCylinder.editCan(0, "stoli_vodka", 750)
    testCylinder.editCan(1, "wildTurkey_bourbon", 750)
    testCylinder.editCan(2, "coca_cola", 2000)
    print(testCylinder.slot.index(testCylinder.can4))
    


#MAIN
def main():
    # infotest()
    # drinktest()
    # waterTest()
    # qTest()
    # dispenseTest()
    # loadTest()
    postest()
    



    
main()