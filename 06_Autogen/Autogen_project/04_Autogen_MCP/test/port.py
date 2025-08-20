import os
from dotenv import load_dotenv
from flask import Flask,jsonify
from pyngrok import ngrok
from flask_cors import CORS

load_dotenv()
NGROK_AUTH_TOKEN=os.getenv("NGROK_AUTH_TOKEN")

app=Flask(__name__)
CORS(app)
@app.route("/api/hello",methods=['GET'])
def hello():
    return jsonify({'message':"Hello, How can I help you?"})


if __name__=="__main__":
    port=7001
    ngrok.set_auth_token(token=NGROK_AUTH_TOKEN)
    public_url=ngrok.connect(port)
    print(f"Public url: {public_url}")
    app.run(port=port)