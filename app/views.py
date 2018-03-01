# Importing flask library
from app import app
from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash
import os
app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'

@app.route('/')
@app.route('/index')
def index():
    #check if the user is already in session, if so, direct the user to survey.html Hint: render_template with a variable
    if 'username' in session:
        username = session['username']
        return render_template('survey.html', username=username)
    return render_template('login.html')

@app.route('/login', methods = ['GET','POST']) # You need to specify something here for the function to get requests
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
    <form action = "" method = "post">
      <p><input type = text name = username/></p>
      <p<<input type = submit value = Login/></p>
   </form>
    
   '''
    # Here, you need to have logic like if there's a post request method, store the username and email from the form into
    # session dictionary
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('email', None)
	return redirect(url_for('index'))



@app.route('/submit-survey', methods = ['GET','POST'])
def submitSurvey():
    username = session['username']
    if request.method == 'POST':
        surveyResponse = {}
        surveyResponse['food'] = request.form.get('color')
        surveyResponse['color'] = request.form.get('food')
        surveyResponse['vacation'] = request.form.get('vacation')
        #get the rest o responses from users using request library Hint: ~3 lines of code
        surveyResponse['fe-before'] = request.form.get('feBefore')
        surveyResponse['fe-after'] = request.form.get('feAfter')
        # if surveyResponse['fe-after'] <= surveyResponse ['fe-before']:
        #    return render_template('base.html')
        return render_template('results.html', surveyResponse=surveyResponse, username=username) # pass in variables to the template
    else:
        session['username'] = session['username'] #check if user in session
        surveyResponse = request.form.get('color')
        surveyResponse = request.form.get('food')
        surveyResponse = request.form.get('vacation')
        #get the rest o responses from users using request library Hint: ~3 lines of code
        surveyResponse['fe-before'] = request.form.get('feBefore')
        surveyResponsec['fe-after'] = request.form.get('feAfter')
        return render_template('results.html', surveyResponse=surveyResponse) # pass in variables to the template

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
