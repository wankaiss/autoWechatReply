# autoWechatReply
auto wechat reply

by using [itchat](https://github.com/littlecodersh/ItChat) to access WeChat, and send messages to AI backend and post AI generated response back to WeChat

## requirements
~~~
pip install -r requirements.txt
~~~

## Dev
script is runable via
~~~
python src/auto_reply.py
~~~

## Todo

* REST API server to handle incoming request
	* /v1/login (GET) return QE code 
* research or write mock for wechat
* add unittest to the code

