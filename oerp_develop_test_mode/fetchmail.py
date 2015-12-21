# -*- coding: utf-8 -*-
#/#############################################################################
#
#    BizzAppDev
#    Copyright (C) 2015-TODAY bizzappdev(<http://www.bizzappdev.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################

from openerp.osv import osv
import logging
from openerp.tools import config
from openerp import models, api, _

_logger = logging.getLogger(__name__)


class fetchmail_server(models.Model):
    _inherit = 'fetchmail.server'

    def get_mode(self, dbname):
        mode = config.get('develop', {}).get(dbname, False) and 'develop' or False
        mode = not mode and config.get('test', {}).get(dbname, False) and 'test' or mode
        return mode

    def button_confirm_login(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if self.get_mode(cr.dbname):
            raise osv.except_osv(
                _("OpenERP Mode"),
                _("You Can not Confirm & Test Because OpenERP is in %s mode.") % self.get_mode(cr.dbname).upper())
        return super(fetchmail_server, self).button_confirm_login(cr, uid, ids, context=context)

    @api.cr_uid_ids_context
    def connect(self, cr, uid, server_id, context=None):
        if isinstance(server_id, (list,tuple)):
            server_id = server_id[0]
        if self.get_mode(cr.dbname):
            raise osv.except_osv(
                _("OpenERP Mode"),
                _("Can not Connect to server because Openerp is in %s mode.") % self.get_mode(cr.dbname).upper())
        return super(fetchmail_server, self).connect(cr, uid, server_id=server_id, context=context)

    def fetch_mail(self, cr, uid, ids, context=None):
       if self.get_mode(cr.dbname):
            raise osv.except_osv(
                _("OpenERP Mode"),
                _("Can not fetchmail because Openerp is in %s mode.") % self.get_mode(cr.dbname).upper())
       return super(fetchmail_server, self).fetch_mail(cr, uid, ids=ids, context=context)

fetchmail_server()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
