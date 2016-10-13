# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import odoo
from odoo import http
from odoo.tools import config
import openerp
import os
import urllib
import urlparse
import re
from odoo.addons.web.controllers.main import Binary
from odoo.http import request


def db_monodb(req):
    # if only one db exists, return it else return False
    return db_redirect(req, True)[0]


def db_redirect(req, match_first_only_if_unique):
    db = False
    redirect = False
    # 1 try the db in the url
    db_url = req.params.get('db')
    if db_url:
        return (db_url, False)

    dbs = db_list(req, True)

    # 2 use the database from the cookie if it's listable and still listed
    cookie_db = req.httprequest.cookies.get('last_used_database')
    if cookie_db in dbs:
        db = cookie_db

    # 3 use the first db if user can list databases
    if dbs and not db and (not match_first_only_if_unique or len(dbs) == 1):
        db = dbs[0]

    # redirect to the chosen db if multiple are available
    if db and len(dbs) > 1:
        query = dict(urlparse.parse_qsl(req.httprequest.query_string, keep_blank_values=True))
        query.update({'db': db})
        redirect = req.httprequest.path + '?' + urllib.urlencode(query)
    return (db, redirect)


def db_list(req, force=False):
    dbs = []
    h = req.httprequest.environ['HTTP_HOST'].split(':')[0]
    d = h.split('.')[0]
    r = odoo.tools.config['dbfilter'].replace('%h', h).replace('%d', d)
    dbs = [i for i in dbs if re.match(r, i)]
    return dbs


class mode(http.Controller):

    @http.route([
                '/web/mode/get_mode',
            ], type='json', auth="none")
    def get_mode(self, req, mode=False, db=False):
        if not db:
            dbs = db_list(req)
            db = dbs and dbs[0] or False
        return config.get(mode, {}).get(db, False)


class cp_Binary(Binary):

    @http.route([
                '/web/binary/company_logo',
                '/logo',
                '/logo.png',
            ], type='http', auth="none")
    def company_logo(self, dbname=None, **kw):
        req = request
        if req.session._db:
            dbname = req.session._db
            uid = req.session._uid
        elif dbname is None:
            dbname = db_monodb(req)

        mode = config.get('develop', {}).get(dbname, False) and 'develop' or False
        mode = not mode and config.get('test', {}).get(dbname, False) and 'test' or mode
        if not mode:
            return super(cp_Binary, self).company_logo(dbname=dbname, **kw)

        # TODO add etag, refactor to use /image code for etag
        module_path = list(os.path.split(__file__)[:-1]) + ["%s_logo.png" % mode]
        image = open(os.path.join(*module_path), 'r')
        image_data = image.read()
        image.close()
        headers = [
            ('Content-Type', 'image/png'),
            ('Content-Length', len(image_data)),
        ]
        return req.make_response(image_data, headers)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
