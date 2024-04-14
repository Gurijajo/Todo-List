from tortoise import Model
from tortoise import fields

class Todo(Model):
    id = fields.IntField(pk=True, index=True)
    title = fields.CharField(max_length=150,  null=False)
    done = fields.BooleanField(default=False, null=False)
    created_at = fields.DatetimeField(null=False, auto_now_add=True)

