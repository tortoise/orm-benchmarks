import os
from decimal import Decimal

from django.db import models
from jsonfield import JSONField


class Journal1(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)


class Journal2(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey(
        "Journal2", related_name="children", on_delete=models.CASCADE, null=True
    )
    related = models.ManyToManyField("Journal2", related_name="related_from")


class Journal3(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.SmallIntegerField(db_index=True)
    text = models.CharField(max_length=255, db_index=True)

    col_float1 = models.FloatField(default=2.2)
    col_smallint1 = models.SmallIntegerField(default=2)
    col_int1 = models.IntegerField(default=2000000)
    col_bigint1 = models.BigIntegerField(default=99999999)
    col_char1 = models.CharField(max_length=255, default="value1")
    col_text1 = models.TextField(default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa")
    col_decimal1 = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal("2.2"))
    col_json1 = JSONField(default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True})

    col_float2 = models.FloatField(null=True)
    col_smallint2 = models.SmallIntegerField(null=True)
    col_int2 = models.IntegerField(null=True)
    col_bigint2 = models.BigIntegerField(null=True)
    col_char2 = models.CharField(max_length=255, null=True)
    col_text2 = models.TextField(null=True)
    col_decimal2 = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    col_json2 = JSONField(null=True)

    col_float3 = models.FloatField(default=2.2)
    col_smallint3 = models.SmallIntegerField(default=2)
    col_int3 = models.IntegerField(default=2000000)
    col_bigint3 = models.BigIntegerField(default=99999999)
    col_char3 = models.CharField(max_length=255, default="value1")
    col_text3 = models.TextField(default="Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa,Moo,Foo,Baa,Waa")
    col_decimal3 = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal("2.2"))
    col_json3 = JSONField(default={"a": 1, "b": "b", "c": [2], "d": {"e": 3}, "f": True})

    col_float4 = models.FloatField(null=True)
    col_smallint4 = models.SmallIntegerField(null=True)
    col_int4 = models.IntegerField(null=True)
    col_bigint4 = models.BigIntegerField(null=True)
    col_char4 = models.CharField(max_length=255, null=True)
    col_text4 = models.TextField(null=True)
    col_decimal4 = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    col_json4 = JSONField(null=True)


test = int(os.environ.get("TEST", "1"))
if test == 1:
    Journal = Journal1
if test == 2:
    Journal = Journal2
if test == 3:
    Journal = Journal3
