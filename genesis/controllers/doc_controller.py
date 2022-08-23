import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController

_logger = logging.getLogger(__name__)

class DocController(http.Controller):

    @http.route("/doc/upload", type="http", auth="public", csrf=False, cors="*")
    def upload_doc(self):
        _logger.info("CONTROLLER DOC => upload")
        if AuthController.is_authorized(request):
            doc = json.loads(request.params["doc"])
            try:
                document = self.create_new_doc(request, doc)
                _logger.info(document.id)
                return request.make_response("Success")
            
            except Exception as e:
                _logger.info(e)
                return Response("Could not upload doc", status=404)

        return Response("Unauthorized", status=401)

    def create_new_doc(self, request, doc):
      return request.env["documents.document"].sudo().create({
                    "display_name": doc["name"],
                    "datas": doc["bytes"],
                    "partner_id": doc["userId"],
                })
