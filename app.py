from flask import Flask, render_template, request
from scheduleduty import scheduleduty

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        render_template('uploading.html')
        return "Placeholder"
