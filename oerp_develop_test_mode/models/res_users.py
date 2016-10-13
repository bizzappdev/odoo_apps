# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.tools import config
from odoo import SUPERUSER_ID
import openerp
DEVELOP = True
TEST = False
ERROR = False


class res_users(models.Model):
    _inherit = 'res.users'

    def __set_from_config_test(self, db):
        cr = openerp.registry(db).cursor()
        config_parameters = self.env["ir.config_parameter"]
        if DEVELOP:
            config_parameters.set_param("develop", DEVELOP)
        if TEST:
            config_parameters.set_param("test", TEST)
        if ERROR:
            config_parameters.set_param("error", ERROR)

        if not config.get('test'):
            config['test'] = {}

        if not config.get('develop'):
            config['develop'] = {}

        if not config.get('error'):
            config['error'] = {}

        if db not in config['test']:
            ir_config_val = self.env["ir.config_parameter"].get_param("test", default=None)
            config['test'][db] = ir_config_val

        if db not in config['develop']:
            ir_config_val = self.env["ir.config_parameter"].get_param(
                "develop", default=None)
            config['develop'][db] = ir_config_val

        if db not in config['error']:
            ir_config_val = self.env["ir.config_parameter"].get_param(
                "error", default=None)
            config['error'][db] = ir_config_val
        cr.close()

    @classmethod
    def check(cls, db, uid, passwd):
        cr = cls.pool.cursor()
        self = api.Environment(cr, uid, {})[cls._name]
        self.__set_from_config_test(db)
        cr.close()
        return super(res_users, self).check(db, uid, passwd)

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        cr = cls.pool.cursor()
        uid = cls._login(db, login, password)
        self = api.Environment(cr, uid, {})[cls._name]
        self.__set_from_config_test(db)
        cr.close()
        return super(res_users, self).authenticate(db, login, password, user_agent_env)

res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
