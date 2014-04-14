import re

from flask import Flask, request
from pyflare import Pyflare


app = Flask(__name__)


@app.errorhandler(Pyflare.APIError)
def api_error_handler(error):
    return (str(error), 400)


@app.route('/update/<email>/<api_key>/<zone>/<domain>')
def update(email, api_key, zone, domain):
    ip = request.remote_addr

    cf = Pyflare(email, api_key)
    resp = cf.rec_load_all(zone)
    records = resp['response']['recs']['objs']
    for record in records:
        if record['name'] == domain:
            hostname = re.sub('\.{0}$'.format(zone), '', domain)
            resp = cf.rec_edit(zone, 'A', record['rec_id'], hostname, ip, ttl=1)
            return ('Successfully updated', 200)
            break

    return ('Hostname not found', 400)


if __name__ == '__main__':
    app.run(debug=True)
