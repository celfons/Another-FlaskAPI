import os
from app import app


if __name__ == '__main__':  
    app.run(threaded=True, port=8080, debug=False)
