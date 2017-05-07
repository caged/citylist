import os
from flask import Flask, render_template
from .db import session
from .models.channel import Channel

app = Flask(__name__)


@app.route('/')
def index():
    channels = session.query(Channel).\
        order_by(Channel.posted_at.desc()). \
        limit(30)

    return render_template('index.html',
                           title='Home',
                           channels=channels)


if __name__ == "__main__":
    print(os.environ)
    app.run(host='0.0.0.0', debug=True, port=3000)
