from iebank_api import app
from config import LocalConfig

app.config.from_object(LocalConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)