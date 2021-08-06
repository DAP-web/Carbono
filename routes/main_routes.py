from flask import render_template


class MainRoutes:
    @staticmethod
    def configure_routes(app):
        @app.route("/")
        def home():
            return render_template("index.html")

        @app.route("/beneficios")
        def beneficios():
            return render_template("beneficios.html")

        @app.route("/acerca")
        def acerca():
            return render_template("acerca.html")

        @app.route("/contactanos")
        def contactanos():
            return render_template("contactanos.html")
