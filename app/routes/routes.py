from flask import Blueprint

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def index():
    """Root URL response."""
    return 'Health Monitoring API is running!'
