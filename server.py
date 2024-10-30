from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify(message=f"Hello, {name}!")

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from Flask!',
        'value': 5454546
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # 모든 네트워크 인터페이스에서 접근 가능하게 설정
