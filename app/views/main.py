# main.py
import os
from utils.create_chart import chart_history_price, chart_price_seasonality
from app import app, ALLOWED_EXTENSIONS
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from bokeh.embed import components
from database.app import get_data_with_filter_name_and_data, get_unique_name_db
from dramatiq_worker.dramatiq_worker import upload_datafile_in_db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/uploading')
@login_required
def uploading():
    return render_template("file_upload_form.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/success', methods=['POST'])
@login_required
def success():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            user_id = current_user.get_id()
            upload_datafile_in_db.send(file_path, user_id)
            return render_template("success.html", name=file.filename)
        return render_template("file_upload_form.html")


@main.route('/chart')
@login_required
def chart():
    unique_names_active = get_unique_name_db()
    return render_template("chart.html", unique_names=unique_names_active)


@main.route("/show_chart", methods=['POST'])
@login_required
def show_chart():
    period_from = datetime.strptime(request.form['from_date'], "%Y-%m-%d")
    period_to = datetime.strptime(request.form['to_date'], "%Y-%m-%d")
    unique_name = request.form['name']
    chart_type = request.form['chart_type']
    data_db = get_data_with_filter_name_and_data(unique_name, period_from, period_to)

    if chart_type == '0':
        lines = chart_history_price(data_db)
        script, div = components(lines)
        return render_template("show_chart.html",
                               the_div=div, the_script=script)
    else:
        lines = chart_price_seasonality(unique_name, period_from, period_to)
        script, div = components(lines)
        return render_template("show_chart.html",
                               the_div=div, the_script=script)
