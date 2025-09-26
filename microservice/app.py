from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_json():
    """Returns a simple JSON response."""
    response_data = {
        "message": "Hello, World!",
        "status": "success",
        "api_version": "1.0"
    }
    # jsonify automatically sets the Content-Type header to application/json
    return jsonify(response_data)

# This block is for local testing only
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)