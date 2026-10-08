from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from services.osint import search_username, search_domain

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-in-production'

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://anormadaise2-ops.github.io"
            ]
        }
    }
)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=['60 per minute'],
    storage_uri='memory://'
)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/privacy')
def privacy():
    return render_template('privacy.html')

@app.get('/api/health')
def health():
    return jsonify(ok=True, service='KAR OSINT')

@app.post('/api/search/username')
@limiter.limit('10 per minute')
def username_search():
    data = request.get_json(silent=True) or {}
    username = str(data.get('username', '')).strip()

    if not username:
        return jsonify(ok=False, error='Pseudo manquant.'), 400

    if len(username) > 80:
        return jsonify(ok=False, error='Pseudo trop long.'), 400

    results = search_username(username)

    return jsonify(
        ok=True,
        query=username,
        count=len(results),
        results=results
    )

@app.post('/api/search/domain')
@limiter.limit('10 per minute')
def domain_search():
    data = request.get_json(silent=True) or {}
    domain = str(data.get('domain', '')).strip()

    if not domain:
        return jsonify(ok=False, error='Domaine manquant.'), 400

    if len(domain) > 253:
        return jsonify(ok=False, error='Domaine trop long.'), 400

    results = search_domain(domain)

    return jsonify(
        ok=True,
        query=domain,
        count=len(results),
        results=results
    )

@app.errorhandler(429)
def rate_limit(_):
    return jsonify(
        ok=False,
        error='Trop de recherches. Réessaie plus tard.'
    ), 429

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False
    )
