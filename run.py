import os
from app import app


if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True, port=8080, debug=False)
