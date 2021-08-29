from flask import Flask, render_template, request
import requests
import json
import smtplib
import ssl

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        token = request.form.get("token")
        # user_name = request.form.get("uname")
        email = request.form.get("email")
        repo_name = request.form.get("rname")

        url = "https://api.github.com/user/repos"

        payload = json.dumps({
            "name": repo_name,
            "homepage": "https://github.com",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        })
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # Autogenerate Email
        smtp_server = 'smtp.gmail.com'
        port = 465

        # Authentication
        sender = 'himshi.test@gmail.com'
        password = 'himshi1234@'

        receiver = email

        # message to be sent
        message = """\
        Subject: Hi There! Repository Creation Status!

        Your Repository created in github..!!!

        Thanks.
        """
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            # sending the mail
            server.sendmail(sender, receiver, message)

        return render_template("output.html", data=str(response.content.decode()))
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
