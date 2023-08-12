from flask import Flask, render_template, request
import requests
import smtplib

my_email = "hollytest@163.com"
password = "FZOWONPNNHIRFAQG"

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    response = requests.get('https://api.npoint.io/a89260239d50fb21145b')
    blogs = response.json()
    print(blogs)
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", flag=False)
    else:
        email_body = f"Name: {request.form['username']}\nEmail: {request.form['email']}\nPhone: {request.form['phone']}\n" \
                     f"Message: {request.form['message']}\n"
        with smtplib.SMTP("smtp.163.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            connection.sendmail(from_addr=my_email,
                                to_addrs="heffann@qq.com",
                                msg=f"Subject:Contact info!\n\n{email_body}")

        return render_template("contact.html", flag=True, name=request.form['username'], email=request.form['email'],
                               phone=request.form['phone'], message=request.form['message'])


@app.route('/post/<int:number>')
def blog(number):
    response = requests.get('https://api.npoint.io/a89260239d50fb21145b')
    blogs = response.json()
    print(blogs[number]['title'])
    return render_template("post.html", blog=blogs[number])


if __name__ == "__main__":
    app.run(debug=True)