from flask import Flask, request, jsonify
from pyngrok import conf, ngrok

app = Flask(__name__)

http_tunnel = ngrok.connect(5000)
tunnels = ngrok.get_tunnels()

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from Flask!',
        'value': 5454546
    }
    return jsonify(data)

if __name__ == '__main__':
    # ngrok 터널 연결 (스크립트가 직접 실행될 때만)
    port = 5000
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok 터널 URL: {public_url}")

    # 애플리케이션 컨텍스트에 public_url 설정 (필요한 경우)
    app.config["public_url"] = public_url

    # Flask 앱 실행 (use_reloader=False 설정)
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)