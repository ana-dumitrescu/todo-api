from marshmallow import Schema, fields

class TodoSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    completed = fields.Bool()
    due_date = fields.DateTime(allow_none=True)
    priority = fields.Str(validate=lambda x: x in ['low', 'medium', 'high'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)