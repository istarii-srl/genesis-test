import base64
import json
from odoo import fields, models
from datetime import datetime, timedelta, date



class AuthToken(models.Model):
  _name = "auth.token"
  _description = "JWT auth token"

  user_id = fields.Many2one(string="Utilisateur", comodel_name="res.users")
  token = fields.Text(string="Token")

  _sql_constraints = [
        ('unique_id_user', 'unique(user_id)', 'This id_user is already in used.'),
    ]

  @staticmethod
  def decode(input):
    return json.loads(base64.urlsafe_b64decode(input+'==').decode('utf-8').replace('=',''))
    
  @staticmethod  
  def encode(input):
    stringAsBytes = input.encode('ascii')
    stringAsBase64 = base64.urlsafe_b64encode(stringAsBytes).decode('utf-8').replace('=','')
    return stringAsBase64 

  @staticmethod
  def jwt_creator(user_id, uid, session_id):
    payload = {"expired": (datetime.now() + timedelta(days=15)).strftime("%d-%m-%y"), "user_id": user_id, "uid": uid, "session_id": session_id}
    return str(AuthToken.encode(json.dumps(payload)))

  def has_expired(self):
    for token in self:
      return datetime.strptime(AuthToken.decode(token.token)["expired"], "%d-%m-%y").date() < date.today()

  def to_map(self):
    for token in self:
      return {
        "id": token.id,
        "user_id": token.user_id.id,
        "token": token.token,
      }