# -*- coding: utf-8 -*-
#/#############################################################################
#
#    BizzAppDev
#    Copyright (C) 2004-TODAY bizzappdev(<http://www.bizzappdev.com>).
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
from openerp.tools.config import config
_logger = logging.getLogger(__name__)
from openerp.models import AbstractModel
from openerp.release import version_info

from openerp.tools import config

if not(version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]):
    config['publisher_warranty_url'] = ''

class publisher_warranty_contract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    def _get_message(self, cr, uid):
        return {}


class publisher_warranty_contract(osv.osv):
    _inherit = 'publisher_warranty.contract'

    def _get_sys_logs(self, cr, uid):

        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            ret =super(publisher_warranty_contract, self)._get_sys_logs(cr, uid)
        return
    def update_notification(self, cr, uid, ids, cron_mode=True,
                            context=None):
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            return super(publisher_warranty_contract, self).update_notification(
                cr, uid, ids, cron_mode=cron_mode, context=context)
        _logger.info("NO More Phoning Home Stuff")
        return True
    def set_notification_update(self, cr, uid, cron_id):
        print "22222222@",cron_id
        if version_info and isinstance(version_info, (list,tuple)) and 'e' == version_info[-1]:
            self.pool.get('ir.cron').write(cr, uid, cron_id, {'active': True})

publisher_warranty_contract()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

