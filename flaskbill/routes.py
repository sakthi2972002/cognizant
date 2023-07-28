from flask import Flask, render_template, url_for , flash , redirect , request
from flaskbill import app , db , bcrypt
from flaskbill.forms import RegistrationForm , LoginForm
from flaskbill.models import User
from flask_login import login_user , current_user, logout_user , login_required
import numpy as np
import pandas as pd 
import joblib 
from sklearn.preprocessing import OrdinalEncoder
import time

with open('previous_encoder.pkl', 'rb') as f:
    previous_enc = joblib.load(f)

with open('icd_encoder.pkl', 'rb')  as f:
    icd_enc = joblib.load(f)

with open('lab_encoder.pkl', 'rb') as f:
    lab_enc = joblib.load(f)

with open('imaging_encoder.pkl', 'rb') as f:
    imaging_enc = joblib.load(f)

with open('best_model.pkl', 'rb') as f:
    model = joblib.load(f)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')





@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        age = int(request.form['age'])
        icd = request.form['ICD-10']
        stay = int(request.form['stay'])
        procedure = int(request.form['procedure'])
        prev_surgeries = request.form['Previous_Surgeries']
        imaging = request.form['Imaging_result']
        lab = request.form['Lab_results']
        insurance_pct = int(request.form['ins_pct'])
        insurance_opt = request.form['ins_opt']

        sample = {
            'Age': age,
            'ICD-10 Code':icd,
            'Previous Surgeries':prev_surgeries,
            'Length_of_Stay':stay,
            'Number_of_Procedures':procedure,
            'Lab_Results':lab,
            'Imaging_Results':imaging
        }

        sample_df = pd.DataFrame(sample,index=[0])
        sample_df['ICD-10 Code'] = icd_enc.transform(sample_df[['ICD-10 Code']])
        sample_df['Lab_Results'] = lab_enc.transform(sample_df[['Lab_Results']])
        sample_df['Previous Surgeries'] = previous_enc.transform(sample_df[['Previous Surgeries']])
        sample_df['Imaging_Results'] = imaging_enc.transform(sample_df[['Imaging_Results']])
        pred = model.predict(sample_df)[0]
        if insurance_opt =='Yes':
            deductions = ((insurance_pct/100)* pred).round(decimals=2)
        else:
            deductions = 0
        balance = (pred - deductions).round(decimals=2)
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%H:%M:%S", named_tuple)
        date = time.strftime("%B %d, %Y", named_tuple)

        def bill_number_generator(starting_number=1000):
         counter = starting_number
         while True:
          yield f"BILL-{counter}"
          counter += 1

# Example usage:
        generate_bill = bill_number_generator(starting_number=1000)

# Generate and display the first three bill numbers
        for _ in range(100):
          bill_number = next(generate_bill)

        
        return render_template('invoice.html',prediction_value=pred, deductions=deductions, balance=balance,current_time=time_string,date=date,first_bill_number=bill_number)
    




@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET' , 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')

                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account",methods = ['GET', 'POST'])
@login_required
def account():
    return render_template('userinfo.html', title='Account')
logout



# @app.route("/invoice" ,methods=['POST','GET'])
# def invoice():
#     print(request.form)
    # int_features=[int(x) for x in request.form.values()]
    # final=[np.array(int_features)]
    # print(int_features)
    # print(final)
    # prediction=model.predict(final) 
    # output= round(prediction[0],2)

    # return render_template('invoice.html',prediction_value=output)


    # return render_template('invoice.html', title='bill')



