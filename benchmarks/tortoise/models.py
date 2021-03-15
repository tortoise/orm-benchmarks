import os
from decimal import Decimal

from tortoise import fields
from tortoise.models import Model

test = int(os.environ.get("TEST", "1"))
if test == 1:

    class Journal(Model):
        timestamp = fields.DatetimeField(auto_now_add=True)
        level = fields.SmallIntField(index=True)
        text = fields.CharField(max_length=255, index=True)


if test == 2:

    class Journal(Model):
        timestamp = fields.DatetimeField(auto_now_add=True)
        level = fields.SmallIntField(index=True)
        text = fields.CharField(max_length=255, index=True)
        parent = fields.ForeignKeyField(
            "models.Journal", related_name="children", null=True
        )
        related = fields.ManyToManyField("models.Journal", related_name="related_from")


if test == 3:

    class Journal(Model):
        timestamp = fields.DatetimeField(auto_now_add=True)
        level = fields.SmallIntField(index=True)
        text = fields.CharField(max_length=255, index=True)

        col_float1 = fields.FloatField(default=2.2)
        col_smallint1 = fields.SmallIntField(default=2)
        col_int1 = fields.IntField(default=2000000)
        col_bigint1 = fields.BigIntField(default=99999999)
        col_char1 = fields.CharField(max_length=255, default="value1")
        col_text1 = fields.TextField(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal1 = fields.DecimalField(12, 8, default=Decimal("2.2"))
        col_json1 = fields.JSONField(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float2 = fields.FloatField(null=True)
        col_smallint2 = fields.SmallIntField(null=True)
        col_int2 = fields.IntField(null=True)
        col_bigint2 = fields.BigIntField(null=True)
        col_char2 = fields.CharField(max_length=255, null=True)
        col_text2 = fields.TextField(null=True)
        col_decimal2 = fields.DecimalField(12, 8, null=True)
        col_json2 = fields.JSONField(null=True)

        col_float3 = fields.FloatField(default=2.2)
        col_smallint3 = fields.SmallIntField(default=2)
        col_int3 = fields.IntField(default=2000000)
        col_bigint3 = fields.BigIntField(default=99999999)
        col_char3 = fields.CharField(max_length=255, default="value1")
        col_text3 = fields.TextField(
            default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa"
        )
        col_decimal3 = fields.DecimalField(12, 8, default=Decimal("2.2"))
        col_json3 = fields.JSONField(
            default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True}
        )

        col_float4 = fields.FloatField(null=True)
        col_smallint4 = fields.SmallIntField(null=True)
        col_int4 = fields.IntField(null=True)
        col_bigint4 = fields.BigIntField(null=True)
        col_char4 = fields.CharField(max_length=255, null=True)
        col_text4 = fields.TextField(null=True)
        col_decimal4 = fields.DecimalField(12, 8, null=True)
        col_json4 = fields.JSONField(null=True)
