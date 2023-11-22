from flask import Blueprint, render_template

# Error blueprint
errors=Blueprint('errors',__name__)

#Handle error 404, route not found 
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

#Handle error 403, No permission
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

#Handle error , Internal server error
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500