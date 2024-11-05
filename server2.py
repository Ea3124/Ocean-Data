from pyngrok import ngrok

if __name__ == '__main__':
    # ngrok 터널 연결
    port = 5000
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok 터널 URL: {public_url}")

    # 여기에 Flask 앱 실행 코드는 제거하고, ngrok 터널만 열리게 합니다.

# http_tunnel = ngrok.connect(5000)
# tunnels = ngrok.get_tunnels()