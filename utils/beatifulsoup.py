from jinja2 import Template
from bs4 import BeautifulSoup

html = '''
<table>
    <thead>
        <tr>
            <th>NOTA</th>
            <th>DATA</th>
            <th>FORNECEDOR</th>
            <th>VALOR</th>
        </tr>
    </thead>
    <tbody>
        {% for d in data %}
        <tr>
            <td>{{ d['nfe'] }}</td>
            <td>{{ d['date'] }}</td>
            <td>{{ d['supplier'] }}</td>
            <td>{{ d['price'] }}</td>
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>R$5.290</td>
        </tr>
    </tfoot>
</table>
'''

template = Template(html)
data = [
    {'nfe': 251, 'date': '25/jan', 'supplier': 'ELETROMAR', 'price': 'R$ 1.570,10'},
    {'nfe': 102, 'date': '28/jan', 'supplier': 'PESA', 'price': 'R$ 2.415,19'}
]

res = template.render(data=data)
soup = BeautifulSoup(res, 'html.parser')

print(soup.prettify())
