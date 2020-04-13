import datetime

from rest_framework import serializers


class TimestampField(serializers.Field):
    def to_representation(self, value):
        epochZero = datetime.datetime(1970, 1, 1, tzinfo=value.tzinfo)
        return str(int((value - epochZero).total_seconds()))
