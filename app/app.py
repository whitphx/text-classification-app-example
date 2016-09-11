import os
from flask import Flask, request, make_response, jsonify
from decorators import crossdomain
from model import Model


env = os.environ.get('FLASK_ENV')
if env == 'production':
    debug = False
else:
    debug = True
port = 5000

app = Flask(__name__, static_url_path='')

model = Model.restore()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/classify', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*' if debug else None)
def classify():
    data = request.json
    if data is None or u'content' not in data:
        response = make_response()
        response.status_code = 400
        return response

    content = data[u'content']
    if type(content) == unicode:
        content = content.encode('utf8')

    response = jsonify(model.get_result(content))
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=debug, port=port)
