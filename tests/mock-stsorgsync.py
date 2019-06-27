import flask
app = flask.Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=["POST", "GET"])
@app.route('/<path:path>', methods=["POST", "GET"])
def catch_all(path):
    if flask.request.json:
        app.logger.warn(flask.request.json)
    return flask.jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
