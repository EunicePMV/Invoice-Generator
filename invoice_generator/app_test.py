import requests

url = 'http://192.168.1.7:5000/'

data = {'name' : 'Paaralan',
        'address' : {'house_num': '123',
                     'street': 'Makisig St.',
                     'barangay': 'Brgy. Malusog',
                     'city': 'Mabuhay City'},
        'product': {'keyboard': 500,
                    'mouse': 700,    
                    'mousepad': 350},
        'quantity' : {'keyboard': 1,
                      'mouse': 2,
                      'mousepad': 3}

    }

html = requests.post(url, json=data)
with open('invoice.pdf', 'wb') as f:
	f.write(html.content)