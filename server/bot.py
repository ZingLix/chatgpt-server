import json, os
from flask import Flask,  request
from revChatGPT.V3 import Chatbot
import traceback
import asyncio
import time

try:
    chat = Chatbot(api_key=os.environ['OPENAI_API_KEY'])
except Exception as e:
    print(traceback.format_exc())
    print("chatgpt login failed")

last_time = 0

app = Flask(__name__)


@app.route("/chatgpt", methods=["POST"], strict_slashes=False)
def chatgpt():
    try:
        req = request.json
        text = req["text"].replace("\\","").strip()
        text = text.replace("/","").strip()
        print("gpt recv: {}".format(text))
        if text=="重置":
            chat.reset()
            return json.dumps({"text": "已重置"})
        global last_time
        cur = time.time()
        if cur - last_time>180:
            chat.reset()
            print("new conversation")
        last_time = cur
        msg = ""
        response = chat.ask(text)
        print("send: {}".format(response))
        msg = response
        return json.dumps({"text": msg})
    except Exception as e:
        print(traceback.format_exc())
        return json.dumps({"text": ("try again \n"+ str(e))[:100]})


app.run(host='0.0.0.0', port=47526, threaded=False)
