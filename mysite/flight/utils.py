# import json
# import datetime
# from django.core.serializers.json import DjangoJSONEncoder

# class DatetimeEncoder(json.JSONEncoder):

#     def default(self, obj):
#         pylint:disable=E0202
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         return super(DecimalEncoder, self).default(obj)

 