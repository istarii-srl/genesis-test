import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController

_logger = logging.getLogger(__name__)

class DocController(http.Controller):

    @http.route("/doc/upload/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def upload_doc(self, employee_id):
        _logger.info("CONTROLLER DOC => upload")
        if AuthController.is_authorized(request):
            doc = json.loads(request.params["doc"])
            try:
                self.create_new_doc(request, doc, employee_id)
                return request.make_response(json.dumps("Success"))
            
            except Exception as e:
                _logger.info(e)
                return Response("Could not upload doc", status=404)

        return Response("Unauthorized", status=401)

    def create_new_doc(self, request, doc, employee_id):
        employee = request.env["hr.employee"].sudo().browse(employee_id)
        if not employee.folder_id:
            employee_folder = request.env["documents.folder"].sudo().search([("name", "=", employee.name)])
            if not employee_folder:
                employee_folder = request.env["documents.document"].sudo().create({
                    "name": employee.name,
                })
            employee.folder_id = employee_folder.id
        
        new_doc = request.env["documents.document"].sudo().create({
                    "datas": doc["bytes"],
                    "partner_id": employee.address_home_id.id,
                    "folder_id": employee.folder_id.id,
                })

        attachment = request.env['ir.attachment'].sudo().browse(new_doc.attachment_id.id)
        attachment.name = doc["name"]
