from flask import Flask

# "__name__" == "__main__"
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"
@app.route("/sobre")
def sobre():
    return"página sobre!"
if __name__ == "__main__":
    app.run(debug=True)
