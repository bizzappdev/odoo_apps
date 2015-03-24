# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request



class Website(openerp.addons.website.controllers.main.Website):
    #------------------------------------------------------
    # View
    #------------------------------------------------------

    @http.route('/website/info', type='http', auth="user", website=True)
    def website_info(self):
        try:
            request.website.get_template('website.info').name
        except Exception, e:
            return request.registry['ir.http']._handle_exception(e, 404)
        irm = request.env()['ir.module.module'].sudo()
        apps = irm.search([('state','=','installed'),('application','=',True)])
        modules = irm.search([('state','=','installed'),('application','=',False)])
        values = {
            'apps': apps,
            'modules': modules,
            'version': openerp.service.common.exp_version()
        }
        return request.render('website.info', values)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
