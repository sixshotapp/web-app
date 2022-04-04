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
    if session['role'] == 'employee':
        isEmployee = 1
    else:
        isEmployee = 0
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

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
