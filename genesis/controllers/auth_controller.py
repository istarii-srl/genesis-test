from ...token_auth.controllers.auth_controller import AuthController


class EmployeeAuthController(AuthController):

    def _prepare_user_data(self, partner_id, token):
        data = super()._prepare_user_data(partner_id, token)
        employee_ids = partner_id.employee_ids
        if len(employee_ids == 1):
            data["employee_id"] = employee_ids[0].id