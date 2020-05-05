from marshmallow import Schema, fields, ValidationError, validate


# Category #Customer #Cart #Product #Texts #News
class CategorySchema(Schema):
    id = fields.String(required=True)
    title = fields.String(required=True, validate=validate.Length(min=2, max=512))
    slug = fields.String(required=True, validate=validate.Length(min=2, max=512))
    description = fields.String(validate=validate.Length(min=0, max=2048))
    subcategories = fields.List(fields.Nested("self", exclude=['subcategories', 'parent']))
    parent = fields.Nested("self", exclude=['subcategories', 'parent'])

