from flask import Flask, send_file

app = Flask(__name__)
# send file as requested
@app.route("/<path:filename>")
def serve_file(filename):
    return send_file(filename)

if __name__ == "__main__":
    app.run(host="172.31.24.141", port=80)
