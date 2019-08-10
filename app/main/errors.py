from . import main
from flask import request,render_template,jsonify


@main.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response=jsonify({'error',404})
        response.status=404
        return response
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response=jsonify({'error',500})
        response.status=500
        return response
    return render_template('500.html'), 500
