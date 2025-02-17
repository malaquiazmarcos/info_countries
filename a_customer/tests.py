from django.test import TestCase

list = [{'name': 'Brasil'}, {'name': 'Argentina'}, ]

order_list = sorted(list, key=lambda x : x['name'] )

print(order_list)

currencies = {'EUR': {'name': 'Euro', 'symbol': '€'}}

def currencies_s(currencies):
    code = None

    for currencie in currencies.values():
        code = currencie['symbol']
    
    return code


code = currencies_s(currencies)
print(code)



