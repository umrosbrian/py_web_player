# Background

This is my simplified adaptation of [wupanhao/py-web-player](https://github.com/wupanhao/py-web-player), which is written for Python 2.  I made tweaks to `webplayer.py` by removing Chinese? characters and adapting it to Python 3.

# Running the server

As normal with tinkering with Flask apps, you'll want to CD to the repo and execute `export FLASK_APP="$PWD/webplayer.py"` and `export FLASK_DEBUG=1` so that you can issue `flask run` to start the server.