# External Imports
# from crypt import methods
from flask import Flask, flash, render_template, redirect, request, redirect, session
from flask_bcrypt import Bcrypt
from global_var import DrinkInfo, EmployeeInfo, IngredientInfo, DrinkInfo
from flask_sqlalchemy import SQLAlchemy

# Local Imports
from database import db, Employees, Users, Credentials, Drinks, Ingredients
from hardware_interfacing.dispenser import *

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///6shot_db.db'
app.config.update(SESSION_COOKIE_SAMESITE = "None", SESSION_COOKIE_SECURE = True)
# db = SQLAlchemy(app)
db.init_app(app)
db.app = app

@app.route('/', methods=['POST', 'GET'])
def index():
    '''
    This function gets the data from the user input and checks to see if it is valid.
    If the information is valid, it will store them in the database. If not, it will throw an error.
    '''
    if request.method == 'POST':
        if "return-to-login" in request.form:
            return redirect('/')
            
        first_name = request.form.get("firstName", False)
        last_name = request.form.get("lastName", False)
        email = request.form.get("email", False)
        password = request.form.get("password", False)
        try:
            if (len(first_name) > 20):
                flash('First name has too many characters.')
                return redirect('/register')
            elif (len(last_name) > 20):
                flash('Last name has too many characters.')
                return redirect('/register')
            elif (len(email) > 30):
                flash('Email has too many characters.')
                return redirect('/register')
            elif (len(password) > 30):
                flash('Password has too many characters.')
                return redirect('/register')
        except Exception:
            flash('Error, please try again.')
            return redirect("/register")

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
                # flash('Thank you for creating your account!')
                return redirect('/')
            else:
                flash('Email entered already has an account associated.')
                return redirect('/register')
        except Exception:
            flash('Error, could not create account. Please try again.')
            return redirect("/register")
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    '''
    This function will get the data from the user input and see if it is a valid
    email and password, allowing then to login.
    '''
    if request.method == 'POST':
        if "email" in request.form:
            user_email = request.form['email']
            user_password = request.form['password']
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
                        return redirect('/menu')
                    else:
                        session['id'] = check_user.id
                        session['email'] = check_user.email
                        session['password'] = check_user.password
                        session['first_name'] = check_employee.first_name
                        session['last_name'] = check_employee.last_name
                        session['role'] = 'employee'
                        return redirect('/employee_menu')
                else:
                    flash('Username and/or Password does not exist!')
                    return redirect('/')
            except Exception:
                flash('Error logging in, please try again.')
                return redirect("/")
    else:
        return render_template('menu.html')

@app.route('/employee_menu')
def employee_menu():
    return render_template('employee_menu.html')

@app.route('/custom_drink')
def custom_drink():
    return render_template('custom_drink.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # if "change-profile" in request.form:
    #     change_first_name = request.form["changeFirstName"]
    #     change_last_name = request.form["changeLastName"]
    #     change_email = request.form["changeEmail"]
    #     change_password = request.form["changePassword"]
    #     try:
    #         if (change_first_name != ''):
    #             user = Users.query.filter_by(id=session['id']).first()
    #             user.first_name = change_first_name
    #             db.session.commit()
    #             session['first_name'] = change_first_name
    #             flash('First name changed successfully.')
    #             # return redirect('/profile')

    #         if (change_last_name != ''):
    #             user = Users.query.filter_by(id=session['id']).first()
    #             user.last_name = change_last_name
    #             db.session.commit()
    #             session['last_name'] = change_last_name
    #             flash('Last name changed successfully.')
    #             # return redirect('/profile')

    #         # try:
    #         #     if (change_username != ''):
    #         #         user = Users.query.filter_by(id=session['id']).first()
    #         #         user.username = change_username
    #         #         db.session.commit()
    #         #         session['username'] = change_username
    #         #         flash('Username changed successfully.')
    #         #         # return redirect('/profile')
    #         # except Exception:
    #         #     flash('Username is taken, please try different one.')

    #         if (change_email != ''):
    #             user = Users.query.filter_by(id=session['id']).first()
    #             user.email = change_email
    #             db.session.commit()
    #             session['email'] = change_email
    #             flash('Email changed successfully.')
    #             # return redirect('/profile')

    #         if (change_password != ''):
    #             user = Users.query.filter_by(id=session['id']).first()
    #             change_password = bcrypt.generate_password_hash(change_password).decode('utf-8')
    #             user.password = change_password
    #             db.session.commit()
    #             session['password'] = change_password
    #             flash('Password changed successfully.')
    #             # return redirect('/profile')

    #         return redirect('/profile')
    #     except Exception:
    #         flash('Error changing profile, please try again.')
    #         return redirect("/profile") 

    # else:
    #     # return render_template('profile.html', horoscope = session['horoscope)
    #     current_user = Users.query.filter_by(id = session['id']).first()
    #     last_date = current_user.last_created
    #     if not last_date or last_date.date() != date.today() or not session['songs']:
    #         # print(session['horoscope'])
    #         profile_playlist = generateHoroPlaylist(session['horoscope'])
    #         current_user.last_created = date.today()
    #         current_user.daily_playlist = song_to_dict(profile_playlist)
    #         session['daily_playlist'] = current_user.daily_playlist
    #         db.session.commit()
    #     else:
    #         # print("getting daily playlist for " + session['username'])
    #         profile_playlist = getDailyPlaylist()
    return render_template('profile.html', user_info = session)

@app.route('/employee_profile', methods=['POST', 'GET'])
def employee_profile():
    if request.method == 'POST':
        if "change-profile" in request.form:
            change_first_name = request.form["changeFirstName"]
            change_last_name = request.form["changeLastName"]
            change_email = request.form["changeEmail"]
            check_password = request.form["checkPassword"]
            change_password = request.form["changePassword"]
            try:
                employee = Employees.query.filter_by(id = session['id']).first()
                if (change_first_name != '' and change_first_name != employee.first_name):
                    employee.first_name = change_first_name
                    db.session.commit()
                    session['first_name'] = change_first_name
                    flash('First name changed successfully.')

                if (change_last_name != '' and change_last_name != employee.last_name):
                    employee.last_name = change_last_name
                    db.session.commit()
                    session['last_name'] = change_last_name
                    flash('Last name changed successfully.')

                try:
                    if (change_email != ''):
                        check_email = Credentials.query.filter_by(email = change_email).first()
                        if check_email is None:
                            credential = Credentials.query.filter_by(id = session['id']).first()
                            credential.email = change_email
                            db.session.commit()
                            session['email'] = change_email
                            flash('Email changed successfully.')
                        else:
                            flash('There is already an account associated with that email.')
                except Exception:
                    flash('Error with changing email. Please try again.')

                if (check_password != '' and change_password != ''):
                    credential = Credentials.query.filter_by(id = session['id']).first()
                    if bcrypt.check_password_hash(credential.password, check_password):
                        change_password = bcrypt.generate_password_hash(change_password).decode('utf-8')
                        credential.password = change_password
                        db.session.commit()
                        session['password'] = change_password
                        flash('Password changed successfully.')
                    else:
                        flash('Old password does not match.')

                return redirect('/employee_profile')
            except Exception:
                flash('Error changing profile, please try again.')
                return redirect("/employee_profile") 
    else:
        return render_template('employee_profile.html', user_info = session)

@app.route('/employees', methods=['POST', 'GET'])
def employees():
    if request.method == 'POST':
        if "add-employee" in request.form:
            new_employee = request.form.get("addEmployeeEmail")
            try:
                if new_employee != '':
                    # credentials = Credentials.query.filter_by(email = new_employee).first().id
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
    
@app.route('/ingredients', methods=['POST', 'GET'])
def ingredients():
    if request.method == 'POST':
        if "edit-ingredient" in request.form:
            change_name = request.form["changeName"]
            change_availability = request.form.get("changeAvailability")
            change_pump = request.form.get("changePump")
            change_alcohol = request.form.get("ChangeAlcohol")
            ingredient_id = request.form.get("ingredientID")
            try:
                ingredient = Ingredients.query.filter_by(id = ingredient_id).first()
                change_availability = ingredient.available if change_availability == None else 1 if change_availability == "1" else 0
                change_pump = ingredient.pump if change_pump == None else change_pump
                change_alcohol = 0 if change_alcohol == "" else change_alcohol

                if (change_name == ingredient.name and change_availability == ingredient.available and change_pump == ingredient.pump and change_alcohol == ingredient.alcohol):
                    flash('No changes made.')
                else:
                    if (change_name != ingredient.name):
                        ingredient.name = change_name
                        db.session.commit()
                        flash('Name changed successfully.')

                    if (change_availability != ingredient.available):
                        ingredient.available = change_availability
                        db.session.commit()
                        flash('Availability changed successfully.')

                    if (change_pump != ingredient.pump):
                        check_pump = Ingredients.query.filter_by(pump = change_pump).first()
                        if check_pump is None or check_pump.pump == -1:
                            ingredient.pump = change_pump
                            db.session.commit()
                            flash('Pump changed successfully.')
                        else:
                            flash('Error adding ingredient, pump is taken.')

                    if (change_alcohol != ingredient.alcohol):
                        ingredient.alcohol = change_alcohol
                        db.session.commit()

                return redirect('/ingredients')
            except Exception:
                flash('Error updating ingredient, please try again.')
            return redirect("/ingredients") 

        elif "add-ingredient" in request.form:
            name = request.form.get("InputName")
            availability = request.form.get("inputAvailability")
            pump = request.form.get("inputPump")
            alcohol = request.form.get("InputAlcohol")
            try:
                alcohol = 0 if alcohol == "" else alcohol
                check_pump = Ingredients.query.filter_by(pump = pump).first()
                if check_pump is None or check_pump.pump == -1:
                    add_ingredient = Ingredients(name = name,
                                                available = availability,
                                                pump = pump,
                                                alcohol = alcohol)
                    db.session.add(add_ingredient)
                    db.session.commit()
                    return redirect("/ingredients") 
                else:
                    flash('Error adding ingredient, pump is taken.')
                    return redirect("/ingredients")
            except Exception:
                flash('Error adding ingredient, please try again.')
                return redirect("/ingredients") 

        elif "remove-ingredient" in request.form:
            remove_ingredient = request.form["remove-ingredient"]
            try:
                ingredient = Ingredients.query.filter_by(name = remove_ingredient).first()
                db.session.delete(ingredient)
                db.session.commit()
                flash(remove_ingredient + ' was removed!')
                return redirect('/ingredients')

            except Exception:
                flash("Error, couldn't remove ingredient.")
                return redirect("/ingredients")

    ingredients = []
    for ingredient in Ingredients.query.all():
        new_ingredient = IngredientInfo()
        new_ingredient.id = ingredient.id
        new_ingredient.name = ingredient.name
        new_ingredient.available = ingredient.available
        new_ingredient.pump = ingredient.pump
        new_ingredient.alcohol = ingredient.alcohol
        ingredients.append(new_ingredient)
    ingredients.sort(reverse=True, key=lambda x: x.pump)
    return render_template('ingredients.html', ingredients = ingredients)

@app.route('/employee_drinks', methods=['POST', 'GET'])
def employee_drinks():
    if request.method == 'POST':
        if "edit-drink" in request.form:
            change_name = request.form["changeName"]
            change_price = request.form.get("ChangePrice")
            change_bev1 = request.form.get("ChangeBev1")
            change_bev2 = request.form.get("ChangeBev2")
            change_bev3 = request.form.get("ChangeBev3")
            change_bev4 = request.form.get("ChangeBev4")
            drink_id = request.form.get("drinkID")
            try:
                drink = Drinks.query.filter_by(id = drink_id).first()
                # print(change_price)
                # print(drink.price)
                # # change_price = drink.available if change_price == None else 0
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

                return redirect('/employee_drinks')
            except Exception:
                flash('Error updating drink, please try again.')

            return redirect("/employee_drinks") 

        elif "add-drink" in request.form:
            name = request.form.get("InputName")
            price = request.form.get("InputPrice")
            bev1 = request.form.get("InputBev1")
            bev2 = request.form.get("InputBev2")
            bev3 = request.form.get("InputBev3")
            bev4 = request.form.get("InputBev4")
            try:
                check_name = Drinks.query.filter_by(name = name).first()
                if check_name is None:
                    add_drink = Drinks(name = name,
                                        price = price,
                                        bev1 = bev1,
                                        bev2 = bev2,
                                        bev3 = bev3,
                                        bev4 = bev4)
                    db.session.add(add_drink)
                    db.session.commit()
                    return redirect("/employee_drinks") 
                else:
                    flash('Error adding drink, name is taken.')
                    return redirect("/employee_drinks")
            except Exception:
                flash('Error adding drink, please try again.')
                return redirect("/employee_drinks") 

        elif "remove-drink" in request.form:
            remove_drink = request.form["remove-drink"]
            try:
                drink = Drinks.query.filter_by(id = remove_drink).first()
                db.session.delete(drink)
                db.session.commit()
                flash(remove_drink + ' was removed!')
                return redirect('/employee_drinks')

            except Exception:
                flash("Error, couldn't remove drink.")
                return redirect("/employee_drinks")

    drinks = []
    for drink in Drinks.query.all():
        print(drink.name)
        new_drink = DrinkInfo()
        new_drink.id = drink.id
        new_drink.name = drink.name
        new_drink.price = drink.price
        new_drink.bev1 = drink.bev1
        new_drink.bev2 = drink.bev2
        new_drink.bev3 = drink.bev3
        new_drink.bev4 = drink.bev4
        new_drink.bev5 = drink.bev5
        new_drink.bev6 = drink.bev6
        drinks.append(drink)
    drinks.sort()

    ingredients = []
    for ingredient in Ingredients.query.all():
        ingredients.append(ingredient.name)
    ingredients.sort()

    return render_template('employee_drinks.html', ingredients = ingredients, drinks = drinks)

@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    testDrink = loadDrink(2)
    testDrink.info()
    # testCylinder = cylinder()
    # testCylinder.editCan("jackdaniels", 750)
    # testCylinder.editCan("coke")
    
    app.run(debug=True)
