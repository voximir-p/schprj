from flask import Flask, send_file

app = Flask(__name__)
@app.route("/tiktokZyNtN47qQxUls7qm50zRZKugGykimdtK.txt", methods=["GET"])
def verify():
    return send_file("tiktokZyNtN47qQxUls7qm50zRZKugGykimdtK.txt")

if __name__ == "__main__":
    app.run(host="172.31.24.141", port=80)
