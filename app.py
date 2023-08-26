import os
from os.path import join, dirname
from flask import jsonify
from dotenv import load_dotenv
from factory import build

app = build()

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    port = os.getenv('APP_PORT')
    print("Run server in port:", port)
    app.run(debug=True, host='0.0.0.0', port=port)


@app.errorhandler(Exception)
def errorhandler(e):
    return jsonify({
        "code": e.code,
        "status": "ERROR",
        "msg": str(e),
        "name": e.name
    }), e.code
