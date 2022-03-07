# External Imports
from flask import Flask, flash, render_template, redirect, request, redirect, session
from flask_bcrypt import Bcrypt
from global_var import EmployeeInfo

# Local Imports
from database import db, Employees, Users, Credentials, Drinks, Ingredients

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///6shot_db.db'
app.config.update(SESSION_COOKIE_SAMESITE = "None", SESSION_COOKIE_SECURE = True)
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

@app.route('/profile')
def profile():
    return render_template('profile.html', user_info = session)

        # if "change-profile" in request.form:
        #     change_first_name = request.form["changeFirstName"]
        #     change_last_name = request.form["changeLastName"]
        #     change_username = request.form["changeUsername"]
        #     change_email = request.form["changeEmail"]
        #     change_password = request.form["changePassword"]
        #     change_birthday = request.form.get("changeBirthday", False)
        #     if (change_birthday != ''):
        #         new_horoscope = horoscope_api.getHoroscope(change_birthday)
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

        #         try:
        #             if (change_username != ''):
        #                 user = Users.query.filter_by(id=session['id']).first()
        #                 user.username = change_username
        #                 db.session.commit()
        #                 session['username'] = change_username
        #                 flash('Username changed successfully.')
        #                 # return redirect('/profile')
        #         except Exception:
        #             flash('Username is taken, please try different one.')

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

        #         if (change_birthday != ''):
        #             user = Users.query.filter_by(id=session['id']).first()
        #             user.birthday = change_birthday
        #             user.horoscope = new_horoscope
        #             db.session.commit()
        #             session['birthday'] = change_birthday
        #             session['horoscope'] = new_horoscope
        #             flash('Birthday changed successfully.')
        #             # return redirect('/profile')

        #         return redirect('/profile')
        #     except Exception:
        #         flash('Error changing profile, please try again.')
        #         return redirect("/profile") 

        # else:
        #     # return render_template('profile.html', horoscope = session['horoscope)
        #     my_desc = Horoscopes.query.filter_by(horoscope=session['horoscope']).first().description
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
        #     return render_template('profile.html',
        #                         #    user_info=session,
        #                         my_desc=my_desc,
        #                         playlist=profile_playlist)

@app.route('/employee_profile')
def employee_profile():
    return render_template('employee_profile.html', user_info = session)

@app.route('/employees')
def employees():
    employees = []
    for employee in Employees.query.all():
        new_emp = EmployeeInfo()
        new_emp.first_name = employee.first_name
        new_emp.last_name = employee.last_name
        new_emp.email = Credentials.query.filter_by(id = employee.credential_id).first().email
        employees.append(new_emp)
    return render_template('employees.html', employees = employees)
    
@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
