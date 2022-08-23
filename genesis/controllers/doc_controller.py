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
                return request.make_response("Success")
            
            except Exception as e:
                _logger.info(e)
                return Response("Could not upload doc", status=404)

        return Response("Unauthorized", status=401)

    def create_new_doc(self, request, doc):
        parent_workspace = request.env["documents.folder"].sudo().search([("name", "=", "HR")])
        if not parent_workspace:
            parent_workspace = request.env["documents.document"].sudo().create({
                "name": "HR",
            })
        
        workspace = request.env["documents.folder"].sudo().search([("parent_folder_id", "=", parent_workspace.id), ("name", "=", doc["user"]["name"])])
        if not workspace:
            workspace = request.env["documents.document"].sudo().create({
                "parent_folder_id": parent_workspace.id,
                "name": doc["user"]["name"],
            })
        
        doc_id = request.env["documents.document"].sudo().create({
                    "datas": doc["bytes"],
                    "partner_id": doc["user"]["id"],
                    "folder_id": workspace.id,
                })

        attachment_id = request.env['ir.attachment'].sudo().browse(doc_id.attachment_id.id)
        attachment_id.name = doc["name"]
