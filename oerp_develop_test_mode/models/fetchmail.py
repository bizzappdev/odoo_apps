# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import logging
from odoo.tools import config
from odoo import models, api, _
from odoo import exceptions

_logger = logging.getLogger(__name__)


class fetchmail_server(models.Model):
    _inherit = 'fetchmail.server'

    @api.model
    def get_mode(self, dbname):
        mode = config.get('develop', {}).get(dbname, False) and 'develop' or False
        mode = not mode and config.get('test', {}).get(dbname, False) and 'test' or mode
        error = config.get('error', {}).get(dbname, False) and True or False
        return mode,error

    @api.multi
    def button_confirm_login(self):
        context = self.env.context
        if context is None:
            context = {}
        mode, error = self.get_mode(self.env.cr.dbname)
        if mode:
            if error:
                raise exceptions.UserError(
                    _("Odoo Mode You Can not Confirm & Test Because Odoo is in %s mode.") % mode.upper())
            else:
                _logger.warning('Odoo Mode You can not confirm & Test Because Odoo is in %s mode.' %mode.upper())
                return
        return super(fetchmail_server, self).button_confirm_login()

    @api.multi
    @api.cr_uid_ids_context
    def connect(self):
        if isinstance(server_id, (list, tuple)):
            server_id = server_id[0]
        mode, error = self.get_mode(self.env.cr.dbname)
        if mode:
            if error:
                raise exceptions.UserError(
                    _("Odoo Mode Can not Connect to server because Odoo is in %s mode.") % mode.upper())
            else:
                _logger.warning('Odoo Mode Can not Connect to server because Odoo is in %s mode.' %mode.upper())
                return
        return super(fetchmail_server, self).connect()

    @api.multi
    def fetch_mail(self):
        mode, error = self.get_mode(self.env.cr.dbname)
        if mode:
            if error:
                raise exceptions.UserError(
                    _("Odoo Mode Can not fetchmail because Odoo is in %s mode.") % mode.upper())
            else:
                _logger.warning('Odoo Mode Can not fetchmail because Odoo is in %s mode.' %mode.upper())
                return
        return super(fetchmail_server, self).fetch_mail()

fetchmail_server()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
