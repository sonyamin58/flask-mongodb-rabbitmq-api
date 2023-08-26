import os
from dotenv import load_dotenv
from factory import build

app = build()

if __name__ == '__main__':
    load_dotenv()

    port = os.getenv('APP_PORT')
    app.run(debug=True, host='0.0.0.0', port=port)
