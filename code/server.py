import os
from flask import Flask
from cfenv import AppEnv
from flask import request
from flask import abort

from sap import xssec


app = Flask(__name__)
port = int(os.environ.get('PORT', 3000))

env = AppEnv()
uaa_service = env.get_service(label='xsuaa').credentials

@app.route('/')
def hello():
    # See if Authorization has been set in Headers
    if 'Authorization' not in request.headers:
        abort(403)
    else:
        print('Authorization header exist')
    access_token = request.headers.get('Authorization')[7:]
    security_context = xssec.create_security_context(access_token, uaa_service)
    isAuthorized = security_context.check_scope('uaa.resource')
    print(access_token)
    if not isAuthorized:
         abort(403)
    else:
        print('uaa.resource scope exist')

    clientId = security_context.get_clientid()
    grantType = security_context.get_grant_type()
    return f"Hello World! (Authenticated with ClientId:{clientId} via GrantType:{grantType})"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
