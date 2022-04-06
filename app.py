# External Imports
from crypt import methods
from flask import Flask, flash, render_template, redirect, request, redirect, session
from flask_bcrypt import Bcrypt
from global_var import DrinkInfo, EmployeeInfo, IngredientInfo, DrinkInfo

# Local Imports
from database import db, Employees, Users, Credentials, Drinks, Ingredients

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///6shot_db.db'
app.config.update(SESSION_COOKIE_SAMESITE = None, SESSION_COOKIE_SECURE = True)
db.init_app(app)
db.app = app

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = "welcome!"
    valid = ""
    if request.method == 'POST':
        if "email" in request.form:
            user_email = request.form.get('email', False)
            user_password = request.form.get('password', False)
            try:
                check_user = Credentials.query.filter_by(email = user_email).first()
                if ( (check_user.email == user_email) and
                        (bcrypt.check_password_hash(check_user.password, user_password))):
                    check_employee = Employees.query.filter_by(credential_id = check_user.id).first()
                    if (check_employee is None):
                        session['id'] = check_user.id
                        session['email'] = check_user.email
                        session['password'] = check_user.password
                        get_user = Users.query.filter_by(credential_id = check_user.id).first()
                        session['first_name'] = get_user.first_name
                        session['last_name'] = get_user.last_name
                        session['role'] = 'member'
                        return redirect('/dashboard')
                    else:
                        session['id'] = check_user.id
                        session['email'] = check_user.email
                        session['password'] = check_user.password
                        session['first_name'] = check_employee.first_name
                        session['last_name'] = check_employee.last_name
                        session['role'] = 'employee'
                        return redirect('/dashboard')
                else:
                    msg = "Invalid Username/Password"
                    valid = "is-invalid"
            except Exception:
                msg = "Error logging in, please try again."
                valid = "is-invalid"
    return render_template('index.html', msg=msg, validate=valid)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    isEmployee = 1 if session['role'] == 'employee' else 0
    drinkNames = []
    drinkNames2 = []
    description = ""
    desc = []
    availableIngredients = []
    filter = "Show All"
    if request.method == "POST":
        filter = str(request.form.get('variable', False))
    print(filter)

    for ingredient in Ingredients.query.filter(Ingredients.available == 1):
        availableIngredients.append(ingredient.name)
    for drink in Drinks.query.all():
        if bevCheck(availableIngredients, drink) == 1:
            if filter != "Show All" and bevCheck(filter, drink) == 0:
                continue
            else:
                drinkNames.append(drink.name)
                drinkNames2.append((drink.name).replace(" ", ""))
                if drink.bev1 != None:
                    description += str(drink.bev1)
                if drink.bev2 != None:
                    description += "\n" + str(drink.bev2)
                if drink.bev3 != None:
                    description += "\n" + str(drink.bev3)
                if drink.bev4 != None:
                    description += "\n" + str(drink.bev4)
                desc.append(description.lstrip())
                description = ""

    return render_template('dashboard.html', names=drinkNames,
    names2=drinkNames2, desc=desc, zip=zip, ingredients=availableIngredients,
    isEmployee=isEmployee)

def bevCheck(ingredientsList, drink):
    drinkIngredients = [drink.bev1, drink.bev2, drink.bev3, drink.bev4]
    for ing in drinkIngredients:
        if ing not in ingredientsList:
            return 0
        else:
            return 1

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = "welcome!"
    if request.method == 'POST' and 'reg_firstName' in request.form:
        first_name = request.form.get("reg_firstName", False)
        last_name = request.form.get("reg_lastName", False)
        email = request.form.get("email", False)
        password = request.form.get("password", False)

        try:
            check_email = Credentials.query.filter_by(email = email).first()
            if (check_email is None):
                new_credential = Credentials(email = email,
                                    password = bcrypt.generate_password_hash(password).decode('utf-8'))
                db.session.add(new_credential)
                db.session.commit()
                new_user = Users(first_name = first_name,
                         last_name = last_name,
                         credential_id = Credentials.query.filter_by(email = email).first().id)
                db.session.add(new_user)
                db.session.commit()
            else:
                msg = "email already registered."
        except Exception:
            msg = "error, could not create account. please try again."

    return render_template('register.html', msg=msg)

@app.route('/employee_menu')
def employee_menu():
    return render_template('employee_menu.html')

@app.route('/employees', methods=['POST', 'GET'])
def employees():
    if request.method == 'POST':
        if "add-employee" in request.form:
            new_employee = request.form.get("addEmployeeEmail")
            try:
                if new_employee != '':
                    emp = Users.query.filter_by(credential_id = Credentials.query.filter_by(email = new_employee).first().id).first()
                    add_emp = Employees(first_name = emp.first_name,
                            last_name = emp.last_name,
                            credential_id = emp.credential_id)
                    db.session.add(add_emp)
                    db.session.commit()

                    db.session.delete(emp)
                    db.session.commit()
                return redirect("/employees")
            except Exception:
                flash('Error adding employee, please try again.')
                return redirect("/employees")

        elif "remove-employee" in request.form:
            remove_employee = request.form["remove-employee"]
            try:
                employee = Employees.query.filter_by(credential_id = Credentials.query.filter_by(email = remove_employee).first().id).first()
                add_user = Users(first_name = employee.first_name,
                            last_name = employee.last_name,
                            credential_id = employee.credential_id)

                # update employees table
                db.session.delete(employee)
                # update users friendship
                db.session.add(add_user)
                db.session.commit()
                flash(remove_employee + ' was removed!')
                return redirect('/employees')

            except Exception:
                flash("Error, couldn't remove employee.")
                return redirect("/employees")
    else:
        employees = []
        for employee in Employees.query.all():
            new_emp = EmployeeInfo()
            new_emp.first_name = employee.first_name
            new_emp.last_name = employee.last_name
            new_emp.email = Credentials.query.filter_by(id = employee.credential_id).first().email
            employees.append(new_emp)
        return render_template('employees.html', employees = employees)

@app.route('/drinks', methods=['POST', 'GET'])
def drinks():
    if request.method == 'POST':
        print("bussy")
        if "edit-drink" in request.form:
            print(request.form)
            drink_id = request.form.get("drinkID")
            change_name = request.form.get("changeName")
            change_price = request.form.get("ChangePrice")
            change_bev1 = request.form.get("ChangeBev1")
            change_bev2 = request.form.get("ChangeBev2")
            change_bev3 = request.form.get("ChangeBev3")
            change_bev4 = request.form.get("ChangeBev4")
            print(drink_id, change_name)
            try:
                drink = Drinks.query.filter_by(id = drink_id).first()
                change_bev1 = drink.bev1 if change_bev1 == "-1" else change_bev1
                change_bev2 = drink.bev2 if change_bev2 == "-1" else change_bev2
                change_bev3 = drink.bev3 if change_bev3 == "-1" else change_bev3
                change_bev4 = drink.bev4 if change_bev4 == "-1" else change_bev4

                if (change_name == drink.name and change_price == drink.price and change_bev1 == drink.bev1 and change_bev2 == drink.bev2 and change_bev3 == drink.bev3 and change_bev4 == drink.bev4):
                    flash('No changes made.')

                else:
                    if (change_name != drink.name):
                        drink.name = change_name
                        db.session.commit()
                        flash('Name changed successfully.')

                    if (change_price != drink.price):
                        drink.price = change_price
                        db.session.commit()
                        # flash('Price changed successfully.')

                    if (change_bev1 != drink.bev1):
                        drink.bev1 = change_bev1
                        db.session.commit()
                        flash('Beverage 1 changed successfully for.')

                    if (change_bev2 != drink.bev2):
                        drink.bev2 = change_bev2
                        db.session.commit()
                        flash('Beverage 2 changed successfully.')

                    if (change_bev3 != drink.bev3):
                        drink.bev3 = change_bev3
                        db.session.commit()
                        flash('Beverage 3 changed successfully.')

                    if (change_bev4 != drink.bev4):
                        drink.bev4 = change_bev4
                        db.session.commit()
                        flash('Beverage 4 changed successfully.')

                return redirect('/drinks')
            except Exception:
                flash('Error updating drink, please try again.')

            return redirect("/drinks")

        elif "add-drink" in request.form:
            name = request.form.get("InputName")
            price = request.form.get("InputPrice")
            bev1 = request.form.get("InputBev1")
            vol1 = request.form.get("InputVol1")
            bev2 = request.form.get("InputBev2")
            vol2 = request.form.get("InputVol2")
            bev3 = request.form.get("InputBev3")
            vol3 = request.form.get("InputVol3")
            bev4 = request.form.get("InputBev4")
            vol4 = request.form.get("InputVol4")
            bev5 = request.form.get("InputBev5")
            vol5 = request.form.get("InputVol5")
            bev6 = request.form.get("InputBev6")
            vol6 = request.form.get("InputVol6")
            try:
                check_name = Drinks.query.filter_by(name = name).first()
                if check_name is None:
                    add_drink = Drinks(name = name,
                                        price = price,
                                        bev1 = bev1,
                                        vol1 = vol1,
                                        bev2 = bev2,
                                        vol2 = vol2,
                                        bev3 = bev3,
                                        vol3 = vol3,
                                        bev4 = bev4,
                                        vol4 = vol4,
                                        bev5 = bev5,
                                        vol5 = vol5,
                                        bev6 = bev6,
                                        vol6 = vol6)
                    db.session.add(add_drink)
                    db.session.commit()
                    return redirect("/drinks")
                else:
                    flash('Error adding drink, name is taken.')
                    return redirect("/drinks")
            except Exception:
                flash('Error adding drink, please try again.')
                return redirect("/drinks")

        elif "remove-drink" in request.form:
            remove_drink = request.form.get("remove-drink")
            try:
                drink = Drinks.query.filter_by(id = remove_drink).first()
                db.session.delete(drink)
                db.session.commit()
                flash(remove_drink + ' was removed!')
                return redirect('/drinks')

            except Exception:
                flash("Error, couldn't remove drink.")
                return redirect("/drinks")

    drinksList = []
    drinksList2 = []
    for drink in Drinks.query.all():
        #print(drink.name)
        new_drink = DrinkInfo()
        new_drink.id = drink.id
        new_drink.name = drink.name
        new_drink.price = drink.price
        new_drink.bev1 = drink.bev1
        new_drink.vol1 = drink.vol1
        new_drink.bev2 = drink.bev2
        new_drink.vol2 = drink.vol2
        new_drink.bev3 = drink.bev3
        new_drink.vol3 = drink.vol3
        new_drink.bev4 = drink.bev4
        new_drink.vol4 = drink.vol4
        new_drink.bev5 = drink.bev5
        new_drink.vol5 = drink.vol5
        new_drink.bev6 = drink.bev6
        new_drink.vol6 = drink.vol6
        drinksList.append(drink)
        drinksList2.append(drink.name.replace(" ", ""))
    # drinks.sort()

    ingredients = []
    for ingredient in Ingredients.query.all():
        ingredients.append(ingredient.name)
    ingredients.sort()

    db_drink = Drinks.query.filter_by(name = "testDrink").first()
    #print(db_drink.name)
    #testDrink = loadDrink(db_drink)
    #testDrink.info()
    return render_template('drinks.html', ingredients = ingredients, drinks = drinksList, names = drinksList2, zip=zip)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
