from marshmallow import fields, Schema


class RoleSchema(Schema):
    id_role = fields.UUID()
    role_name = fields.Str()
    role_code = fields.Str()
    login_in_station = fields.Boolean()
    manage_practice_manager = fields.Boolean()
    manage_mp = fields.Boolean()
    manage_nmp = fields.Boolean()
    manage_patient = fields.Boolean()
    manage_sys_admin = fields.Boolean()
    manage_dev = fields.Boolean()
    get_patient = fields.Boolean()
    list_patient = fields.Boolean()
    detail_patient = fields.Boolean()
    manage_treatment = fields.Boolean()
    run_sesion = fields.Boolean()
    user_logout = fields.Boolean()
    app_login = fields.Boolean()
    app_select_patient = fields.Boolean()
    app_detail_patient = fields.Boolean()
    debug_app_hmi = fields.Boolean()
    manage_station = fields.Boolean()
    manage_group = fields.Boolean()
    manage_practice = fields.Boolean()


class RoleUpdateSchema(Schema):
    role_name = fields.Str()
    role_code = fields.Str()
    login_in_station = fields.Boolean()
    manage_practice_manager = fields.Boolean()
    manage_mp = fields.Boolean()
    manage_nmp = fields.Boolean()
    manage_patient = fields.Boolean()
    manage_sysadmin = fields.Boolean()
    manage_dev = fields.Boolean()
    get_patient = fields.Boolean()
    list_patient = fields.Boolean()
    detail_patient = fields.Boolean()
    manage_treatment = fields.Boolean()
    run_sesion = fields.Boolean()
    user_logout = fields.Boolean()
    app_login = fields.Boolean()
    app_select_patient = fields.Boolean()
    app_detail_patient = fields.Boolean()
    debug_app_hmi = fields.Boolean()
    manage_station = fields.Boolean()
    manage_group = fields.Boolean()
    manage_practice = fields.Boolean()


class RoleSchemaList(Schema):
    id_role = fields.UUID()
    role_name = fields.Str()
    role_code = fields.Str()


role_schema_detail = RoleSchema()
role_schema_update = RoleUpdateSchema()
role_schema_list = RoleSchemaList()
