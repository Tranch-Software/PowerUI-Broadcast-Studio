from flask import * 

app = Flask(__name__)
@app.route("/")
def openBroadcaster():
    return render_template("index.html")

app.run(debug=True)