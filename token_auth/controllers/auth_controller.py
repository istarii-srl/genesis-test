import json
import logging
from odoo import http
from odoo.http import request, Response

from ..models.auth_token import AuthToken

_logger = logging.getLogger(__name__)

class AuthController(http.Controller):

    @http.route("/auth/login", type="http", auth="public", csrf=False, cors="*")
    def get_auth(self, **kwarg):
        _logger.info("CONTROLLER LOGIN => get auth")
        email = request.params["email"]
        password = request.params["password"]

        _logger.info("##############")
        _logger.info(request.db)
        _logger.info(request.session.db)

        uid = request.session.authenticate(
            request.session.db, email, password)
        if uid:
            res_user = request.env["res.users"].browse(request.uid)
            user = res_user.partner_id

            if user:
                token = request.env["auth.token"].sudo().search([("user_id", "=", uid)], limit=1)

                if token and token.has_expired():
                    _logger.info("TOKEN EXPIRED")
                    token.token = AuthToken.jwt_creator(user.id, uid, request.session.sid)

                elif not token:
                    _logger.info("NO TOKEN")
                    token = request.env["auth.token"].sudo().create({"user_id": uid, "token": AuthToken.jwt_creator(user.id, uid, request.session.sid)})

                user = user.to_map()
                user["token"] = token.to_map()

                _logger.info("TOKEN => " + str(AuthToken.decode(token.token)))
                _logger.info("USER => " + str(user))
                _logger.info("SESSION ID => " + str(request.session.sid))
                _logger.info("SESSION TOKEN => " + str(res_user._compute_session_token(request.session.sid)))

                response = request.make_response(json.dumps({"user": user, "session_id": request.session.sid}), headers=[("Access-Control-Allow-Headers", "*"), ("Content-Type", "text/html; charset=utf-8"), ("Access-Control-Allow-Origin", "*")])
                # response.set_cookie('auth', request.session.sid, path="/", domain="dev.localhost:8000", secure=True, httponly=False, samesite=None,)
                return response

        return Response("Unauthorized", status_code=401)

    @http.route("/auth/recover", type="http", auth="public", csrf=False, cors="*")
    def recover_auth(self, **kwarg):
        _logger.info("CONTROLLER LOGIN => recover auth")
        if request.httprequest.headers["Authorization"]:
            token = AuthToken.decode(request.httprequest.headers["Authorization"])

            logged = request.env["res.users"].sudo().browse(token["uid"]).partner_id

            if logged and logged.has_access_right():
                token_db = request.env["classpro.auth.token"].sudo().search([("user_id", "=", token["uid"])], limit=1)
                user = logged.user_to_extranet()
                user["token"] = token_db.to_extranet()
                return request.make_response(json.dumps({"user": user}))

            return Response("Bad request", status_code=404)

        return Response("Unauthorized", status_code=401)

class AuthHelper:

  @staticmethod
  def is_authorized(request):
    if request.httprequest.headers["Authorization"]:
      token = AuthToken.decode(request.httprequest.headers["Authorization"])
      res_user = request.env["res.users"].sudo().browse(token["uid"])
      if res_user and res_user.active and token["user_id"] == res_user.partner_id.id:
        token_db = request.env["auth.token"].sudo().search([("user_id", "=", res_user.id)], limit=1)
        if token_db:
          return AuthToken.decode(token_db.token) == token
    return Response("Unauthorized", status_code=401)

  def get_uid(request):
    return AuthToken.decode(request.httprequest.headers["Authorization"])["uid"]

  def get_user_id(request):
    return AuthToken.decode(request.httprequest.headers["Authorization"])["user_id"]