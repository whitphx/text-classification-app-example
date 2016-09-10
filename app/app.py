import os
from flask import Flask, request, make_response, jsonify
from decorators import crossdomain


env = os.environ.get('FLASK_ENV')
if env == 'production':
    debug = False
else:
    debug = True
port = 5000

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/classify', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*' if debug else None)
def classify():
    data = request.json
    print data
    if data is None or u'content' not in data:
        response = make_response()
        response.status_code = 400
        return response

    content = data[u'content']
    response = jsonify({
        'content': content
    })  # echo
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=debug, port=port)
