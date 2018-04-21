import os
import xmlrpc.client

host = os.environ.get('ODOO_HOST')
db = os.environ.get('ODOO_DATABASE')
username = os.environ.get('ODOO_USERNAME')
pwd = os.environ.get('ODOO_PASSWORD')

common = xmlrpc.client.ServerProxy("%s/xmlrpc/2/common" % host)
print(common.version())
uid = common.authenticate(db, username, pwd, {})


models = xmlrpc.client.ServerProxy("%s/xmlrpc/2/object" % host)

from linkedin_scraper import Person
from selenium import webdriver
driver = webdriver.Chrome()
url = input("login and enter when ready")

def execute_kw( *args, **kwargs ):
    return models.execute_kw(db, uid, pwd, *args, **kwargs)

res = execute_kw('res.partner', 'search_read',
    [[['is_company', '=', False], ['customer', '=', True], ['image', '=?', ""], ['x_linkedin', '!=', False]]],
    {'fields': ['name', 'x_linkedin', ], 'limit': 100})

def updateImage(id, pic):
    execute_kw('res.partner', 'write', [[id], {
        'image': pic
    }])

for partner in res:
    try:
        person = Person(partner['x_linkedin'], scrape=False, driver=driver)
        person.scrape(close_on_complete=False)
        updateImage(partner['id'], person.profile_picture.split(',')[1])
        print(person.name, partner['name'])
    except Exception as e:
        print(e)
