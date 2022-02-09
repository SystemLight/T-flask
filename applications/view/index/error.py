from flask import Blueprint, render_template

error_bp = Blueprint('Error', __name__, url_prefix='/error')


@error_bp.route('/404', methods=['GET'])
def error_404():
    return render_template('errors/404.html')


@error_bp.route('/403', methods=['GET'])
def error_403():
    return render_template('errors/403.html')


@error_bp.route('/500', methods=['GET'])
def error_500():
    return render_template('errors/500.html')
