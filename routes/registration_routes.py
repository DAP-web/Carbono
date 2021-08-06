from flask import render_template, request, redirect, session
import requests
from logic.userLogic import UserLogic
import bcrypt


class RegisterRoutes:
    @staticmethod
    def configure_routes(app):
        @app.route("/registration", methods=["GET", "POST"])
        def registration():
            if request.method == "GET":
                return render_template("registration.html")
            elif request.method == "POST":
                logic = UserLogic()

                username = request.form["usuario_reg"]
                email = request.form["correo_reg"]
                password = request.form["contra_reg"]
                cPassword = request.form["contraConf_reg"]
                admin = request.form["adminORClient"]
                nombreTarjeta = request.form["nombreTarjeta"]
                numeroTarjeta = request.form["numeroTarjeta"]
                codigoTarjeta = request.form["codigoTarjeta"]
                vencimientoTarjeta = request.form["vencimientoTarjeta"]

                fechaMesVenc = vencimientoTarjeta.split("-")
                vencimientoTarjeta = str(
                    fechaMesVenc[1]) + "/" + str(fechaMesVenc[0][2:])

                if int(admin) == 0:
                    balance = 15.00
                else:
                    balance = 25.00

                # Verificando tarjeta de credito o paypal
                restapi = "https://credit-card-auth-api-cerberus.herokuapp.com"
                endpoint = "/verify"

                url = f"{restapi}{endpoint}"

                data = {
                    "name": nombreTarjeta,
                    "number": numeroTarjeta,
                    "date": vencimientoTarjeta,
                    "code": codigoTarjeta,
                    "balance": balance  # el valor de la transaccion
                }

                response = requests.post(url, data=data)
                print(response)
                if response.status_code == 200:
                    dataJson = response.json()
                    if dataJson['response'] == '00':
                        print(dataJson)
                    else:
                        print(dataJson)
                        if dataJson['response'] == '05':
                            message = "El código que ha ingresado es incorrecto."
                        elif dataJson['response'] == '07':
                            message = "La fecha que ha ingresado es incorrecta."
                        elif dataJson['response'] == '08':
                            message = "El nombre que ha ingresado es incorrecto."
                        elif dataJson['response'] == '14':
                            message = "El número de tarjeta ingresado es incorrecto."
                        elif dataJson['response'] == '41':
                            message = "Esta tarjeta ha sido denunciada como perdida."
                        elif dataJson['response'] == '43':
                            message = "Esta tarjeta ha sido denunciada como robada. Usted acaba de ser denunciad@ a la policia local."
                        elif dataJson['response'] == '51':
                            message = "Su saldo insuficiente para realizar la transacción."
                        elif dataJson['response'] == '54':
                            message = "Su tarjeta está inactiva. Acércate a tu banco más cercano."
                        elif dataJson['response'] == '61':
                            message = "El valor de la transacción excede el limite de la tarjeta."
                        elif dataJson['response'] == 'QY':
                            message = "El tipo de la tarjeta es inválido."

                        return render_template("registration.html", messageFailureTarjeta=message)

                if password == cPassword:
                    salt = bcrypt.gensalt(rounds=14)
                    epswd = password.encode("utf-8")

                    hashpswd = bcrypt.hashpw(epswd, salt)

                    strSalt = salt.decode("utf-8")
                    strPswd = hashpswd.decode("utf-8")

                    try:
                        rows = logic.insertUser(
                            username, email, strPswd, strSalt, admin)
                    except:
                        message = "¡El correo ingresado ya está registrado!"
                        return render_template("registration.html", message=message)

                    print("Rows affected:", rows, sep=" ")

                    return redirect("login")
                else:
                    message = "Las contraseñas no coinciden. Verifique y vuelva a intentar."
                    return render_template("registration.html", message=message)
