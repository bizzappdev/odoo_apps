# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.tools import config
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ir_mail_server(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def get_mode(self, dbname):
        mode = config.get('develop', {}).get(dbname, False) and 'develop' or False
        mode = not mode and config.get('test', {}).get(dbname, False) and 'test' or mode
        error = config.get('error', {}).get(dbname, False) and True or False
        return mode, error

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False):
        mode, error = self.get_mode(self.env.cr.dbname)
        if mode:
            if error:
                raise UserError(
                    _('Odoo Mode You Can not Send Mail Because Odoo is in %s mode' %mode.upper()))
            else:
                _logger.warning('Odoo Mode You Can not Send Mail Because Odoo is in %s mode' % mode.upper())
            return super(ir_mail_server, self).send_email(
                message, mail_server_id=mail_server_id,
                smtp_server=smtp_server, smtp_port=smtp_port,
                smtp_user=smtp_user, smtp_password=smtp_password,
                smtp_encryption=smtp_encryption, smtp_debug=smtp_debug)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
