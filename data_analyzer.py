from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import data_analyzer  # Import the data_analyzer module

data_analyzer_bp = Blueprint('data_analyzer', __name__)

@data_analyzer_bp.route('/data_analyzer')
def data_analyzer_list():
    # Fetch all data analyzers from the database
    analyzers = data_analyzer.get_all_analyzers()
    return render_template('data_analyzer_list.html', analyzers=analyzers)

@data_analyzer_bp.route('/data_analyzer_detail/<int:analyzer_id>')
def data_analyzer_detail(analyzer_id):
    # Fetch the data analyzer from the database
    analyzer = data_analyzer.get_analyzer(analyzer_id)
    return render_template('data_analyzer_detail.html', analyzer=analyzer)