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
                self.create_new_doc(request, doc)
                return request.make_response(json.dumps("Success"))
            
            except Exception as e:
                _logger.info(e)
                return Response("Could not upload doc", status=404)

        return Response("Unauthorized", status=401)

    def create_new_doc(self, request, doc):
        user = request.env["hr.employee"].browse(doc["user"]["id"])
        if not user.folder_id:
            user_folder = request.env["documents.folder"].sudo().search([("name", "=", user.name)])
            if not user_folder:
                user_folder = request.env["documents.document"].sudo().create({
                    "name": user.name,
                })
            user.folder_id = user_folder.id
        
        doc = request.env["documents.document"].sudo().create({
                    "datas": doc["bytes"],
                    "partner_id": doc["user"]["id"],
                    "folder_id": user.folder_id.id,
                })

        attachment = request.env['ir.attachment'].sudo().browse(doc.attachment.id)
        attachment.name = doc["name"]
