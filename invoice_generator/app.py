from flask import Flask, render_template, send_file, request
import os
import datetime
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dynamic_html():
    current_date = datetime.datetime.now()
    issued_date = current_date.strftime('%B') + " " + "%d, %d" % (current_date.day, current_date.year)

    due_month = current_date.month + 3
    if due_month > 12:
        due_month -= 12
        object_month = datetime.datetime.strptime(str(due_month), '%m')
        due_month = object_month.strftime('%B')
        due_year = current_date.year + 1
        due_date = due_month + ' %d, %d' % (current_date.day, due_year)
    else:
        object_month = datetime.datetime.strptime(str(due_month), '%m')
        due_month = object_month.strftime('%B')
        due_date = due_month + ' %d, %d' % (current_date.day, current_date.year)

    json = request.get_json() or {}

    default_data = {'name' : 'Sintang Paaralan',
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

    name = json.get('name', default_data['name'])
    address = json.get('address', default_data['address'])
    product = json.get('product', default_data['product'])
    quantity = json.get('quantity', default_data['quantity'])

    total = 0
    for value in default_data['product']:
        total += default_data['product'][value] * default_data['quantity'][value]



    rendered = render_template("invoice_template.html",
                           issued_date=issued_date,
                           due_date=due_date,
                           name=name,
                           address=address,
                           product=product,
                           quantity=quantity,
                           total=total)

    html = HTML(string=rendered)
    print(rendered)
    rendered_pdf = html.write_pdf()

    return send_file(
        io.BytesIO(rendered_pdf),
        attachment_filename='invoice.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)