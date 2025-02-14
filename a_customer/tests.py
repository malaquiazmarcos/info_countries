from django.test import TestCase

list = [{'name': 'Brasil'}, {'name': 'Argentina'}, ]

order_list = sorted(list, key=lambda x : x['name'] )

print(order_list)


