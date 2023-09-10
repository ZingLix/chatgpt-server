FROM FROM python:3.11-slim
RUN pip install flask beautifulsoup4 pytz requests kuriyama pymongo pyyaml flask-cors flask-login gevent websocket-client
WORKDIR /project
RUN pip install revChatGPT
COPY ./server/*.py /project/
CMD ["python", "bot.py"]
