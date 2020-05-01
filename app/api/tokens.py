from flask import jsonify, g
from app import db
from app.api.users import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    refresh_token = g.current_user.get_refresh_token()
    access_token = g.current_user.get_access_token()
    db.session.commit()
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonify(tokens)

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
