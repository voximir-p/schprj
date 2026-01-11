from flask import Flask, send_file

app = Flask(__name__)
@app.route("/verify/tiktok0h2WcHjMBYRbT1AukihT6pD2JvElI19D.txt", methods=["GET"])
def verify():
    return send_file("tiktok0h2WcHjMBYRbT1AukihT6pD2JvElI19D.txt")

if __name__ == "__main__":
    app.run(host="172.31.24.141", port=80)
