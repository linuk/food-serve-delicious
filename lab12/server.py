from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<h1>Hellp, world!</h1>"


# Display current time
@app.route('/time')
def getTime():
    time = str(datetime.now())
    return "<center><h1>%s</time></center>" % time


# Display the page with customised hello
@app.route('/hello/<username>')
def customised_hello(username):
    # show the user profile for that user
    return 'Hello %s' % username


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
