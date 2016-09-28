from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from scheduleduty import scheduleduty
import os

print help(scheduleduty)

cwd = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['CSV_DIR'] = os.path.join(cwd, 'csvs')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 Mb


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle requests on index.html"""

    if request.method == 'GET':
        return render_template('index.html')
    else:
        render_template('uploading.html')
        if request.form['schedule_type'] == 'weekly_shifts':
            # Check to ensure optional fields are included for weekly_shifts
            if (not request.form['level_name'] or not
                request.form['multi_name'] or not request.form['num_loops'] or
               not request.form['escalation_delay']):
                    flash('Missing a required field.')
                    return redirect(url_for('index'))
            file = request.files['csvs']
            if valid_csv(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.isdir(app.config['CSV_DIR']):
                    os.mkdir(app.config['CSV_DIR'])
                file.save(os.path.join(app.config['CSV_DIR'], filename))
            importer = scheduleduty.Import(
                'weekly_shifts',
                app.config['CSV_DIR'],
                request.form['api_key'],
                request.form['base_name'],
                request.form['level_name'],
                request.form['multi_name'],
                request.form['start_date'],
                request.form['end_date'],
                request.form['time_zone'],
                request.form['num_loops'],
                request.form['escalation_delay']
            )
        else:
            importer = scheduleduty.Import(
                'standard_rotation',
                app.config['CSV_DIR'],
                request.form['api_key'],
                request.form['base_name'],
                None,
                None,
                request.form['start_date'],
                request.form['end_date'],
                request.form['time_zone'],
                None,
                None
            )
        importer.execute()
        return "Successfully added schedules!"


def valid_csv(filename):
    """Validates that a file is actually a CSV"""

    if filename.rsplit('.', 1)[1] == 'csv':
        return True
    else:
        return False
