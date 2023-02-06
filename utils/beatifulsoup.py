from jinja2 import Template
from bs4 import BeautifulSoup

html = '''
<h1>MADEIREIRA KAMUA LTDA</h1>
<h2>RELATÓRIO DE NOTAS {{ month }} {{ year }} </h2>
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
            <td>{{ d['value'] }}</td>
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td>{{ total }}</td>
        </tr>
    </tfoot>
</table>
'''

# %d/%b

template = Template(html)
data = [
    {'nfe': 251, 'date': '25/jan', 'supplier': 'ELETROMAR', 'value': 'R$ 1.570,10'},
    {'nfe': 102, 'date': '28/jan', 'supplier': 'PESA', 'value': 'R$ 2.415,19'}
]
total = 1

with open('templates/report.html', 'r', encoding='utf-8') as f:
    html_soup = BeautifulSoup(f.read(), 'html.parser')

res = template.render(data=data, total=total, month='JANEIRO', year='2023')
soup = BeautifulSoup(res, 'html.parser')

html_soup.find('body').append(soup)

print(html_soup.prettify())
