from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "content"

if __name__ == "__main__":
    app.run()