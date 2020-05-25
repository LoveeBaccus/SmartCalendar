from flask import Flask, request, render_template
from wtforms import Form, StringField
import plansmart

app = Flask(__name__)

class HomeworkForm(Form):
    subject         = StringField('Subject')
    num_problems    = StringField('Number of Problems')
    q_type          = StringField('Question Type')
    difficulty      = StringField('Difficulty')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = HomeworkForm(request.form)

    if request.method == 'POST':
        data = plansmart.input_to_formatted_data(form.subject, form.num_problems, form.q_type, form.difficulty)
        mins = plansmart.get_data_from_azure(data)
        return render_template('results.html', mins=mins)

    return render_template('index.html', form=form)  

if __name__ == "__main__":
    app.run()
