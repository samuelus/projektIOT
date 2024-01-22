from flask import current_app, render_template, redirect
import os


def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/loginPrompt')
    def login_prompt():
        return render_template('loginPrompt.html')

    @app.route('/zones')
    def zones():
        return render_template('zones.html')

    @app.route('/imprints')
    def imprints():
        return render_template('imprints.html')

    @app.route('/employees')
    def employees():
        return render_template('employees.html')

    @app.route('/reports')
    def reports():
        return render_template('reports.html')

    @app.route('/css/<file_name>')
    def css_files(file_name):
        return current_app.send_static_file("css/"+file_name)

    @app.route('/js/<file_name>')
    def js_files(file_name):
        return current_app.send_static_file("js/" + file_name)

    @app.route('/<path:path>.html')
    def redirect_html(path):
        return redirect("/"+path)
