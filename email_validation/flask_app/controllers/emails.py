from flask_app import app
from flask_app.models import email
from flask import request, redirect, render_template
from babel.dates import format_datetime

@app.route('/emails/create', methods=['POST'])
def process_email():

    if (not email.Email.validate_email(request.form)):
        return redirect('/')

    result = email.Email.create(request.form)
    return redirect('/success')

@app.route('/emails/<int:id>/delete')
def delete_email(id):
    data = {'id': id}
    result = email.Email.delete(data)
    return redirect('/success')

@app.route('/success')
def show_success():
    _emails = email.Email.get_all()
    return render_template('./success.html', emails=_emails)

@app.template_filter('format_datetime')
def _format_datetimevalue(value, format='MM/dd/yy hh:mm:ssa'):
    return format_datetime(value, format)