from flask import Blueprint, render_template
from utils.helpers import login_required

bp = Blueprint('dashboard_controller', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')