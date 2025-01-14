from flask import Blueprint, render_template, request, redirect, url_for, session
from functools import wraps
import recreational_activities  # Import the recreational_activities module

recreational_activities_bp = Blueprint('recreational_activities', __name__)

@recreational_activities_bp.route('/recreational_activities')
def recreational_activities_list():
    # Fetch all recreational activities from the database
    activities = recreational_activities.get_all_activities()
    return render_template('recreational_activities_list.html', activities=activities)

@recreational_activities_bp.route('/recreational_activity_detail/<int:activity_id>')
def recreational_activity_detail(activity_id):
    # Fetch the recreational activity from the database
    activity = recreational_activities.get_activity(activity_id)
    return render_template('recreational_activity_detail.html', activity=activity)