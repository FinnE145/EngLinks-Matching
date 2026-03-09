from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new-student")
def new_student():
    return render_template("input.html")

@app.route("/view-matches")
def view_matches():
    return render_template("matches.html")

if __name__ == "__main__":
    app.run(debug=True)