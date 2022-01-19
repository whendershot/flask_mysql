from flask import request,redirect, session, render_template
from flask_app.models import dojoSurvey
from flask_app import app


@app.route('/process', methods = ['POST'])
def process_survey():
    
    data = {
        'name' : request.form.get('user_name'),
        'location' : request.form.get('dojo_location'),
        'language' : ', '.join(str(i) for i in request.form.getlist('languages')),
        'comment' : request.form.get('comment')
    }
    
    if (not dojoSurvey.DojoSurvey.validate(data)):
        return redirect('/')
    
    session['latest_survey'] = {
        'name' : request.form.get('user_name'),
        'location' : request.form.get('dojo_location'),
        'languages' : request.form.getlist('languages'),
        'comment' : request.form.get('comment')
    }
    dojoSurvey.DojoSurvey.create(data)
    return redirect('/result')

@app.route('/result')
def show_result():
    return render_template('./user_form_display.html', survey=session['latest_survey'])

@app.route('/surveys')
def show_surveys():
    _surveys = dojoSurvey.DojoSurvey.get_all()
    print(_surveys)
    return render_template('./surveys.html', surveys=_surveys)
