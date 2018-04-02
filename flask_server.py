from flask import Flask
from flask import render_template
from flask import request

from bot import repost

app = Flask(__name__)

@app.route('/bot', methods=['POST','GET']) # на этот адрес надо отправлять post, чтобы инициировать репост поста из вк в телеграм
def bot():
    if request.method == 'GET':
        return repost()

@app.route('/') #шаблон index.html пока что нужен только для удобства тестирования. С этой формы отправляется POST в /bot
@app.route('/index')
def index():
    return render_template('index.html')

if __name__== '__main__': app.run()
