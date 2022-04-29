# Setup
Set up venv:
`python3 -m venv .`
Activate venv:
`source ./bin/activate`
Deactivate venv:
`deactivate`
Install libraries:
```sh
pip3 install python-kasa
pip3 install asyncio
pip3 install requests
pip3 install python-dotenv
```

Make sure you update `kasa.env` to include the password and username for TP-Link Cloud.

# Links
- API: https://realpython.com/api-integration-in-python/
- Kasa API: https://github.com/arallsopp/tp-link-smart-switch-web-client-/blob/master/script.js
- Python Kasa: https://python-kasa.readthedocs.io/en/latest/smartplug.html
