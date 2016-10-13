# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.tools import config


class project_configuration(models.TransientModel):
    _inherit = 'base.config.settings'

    test = fields.Boolean('Active Test Mode')
    develop = fields.Boolean('Active Develop Mode')
    error = fields.Boolean('Raise error for incoming/outgoing mail')

    @api.multi
    def get_default_test(self, ids):
        test = config.get('test', {}).get(self.env.cr.dbname, False)
        return {'test': test or False}

    @api.multi
    def get_default_develop(self, ids):
        develop = config.get('develop', {}).get(self.env.cr.dbname, False)
        return {'develop': develop or False}

    @api.multi
    def get_default_error(self, ids):
        error = config.get('error', {}).get(self.env.cr.dbname, False)
        return {'error': error or False}

    def set_error(self):
        if not config.get('error'):
            config['error'] = {}
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config['error'][self.env.cr.dbname] = record.error
            config_parameters.set_param(
                "error", record.error or '',
                )

    def set_develop(self):
        if not config.get('develop'):
            config['develop'] = {}
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config['develop'][self.env.cr.dbname] = record.develop
            config_parameters.set_param(
                "develop", record.develop or '',
                )

    def set_test(self):
        if not config.get('test'):
            config['test'] = {}
        config_parameters = self.env["ir.config_parameter"]
        for record in self:
            config['test'][self.env.cr.dbname] = record.test
            config_parameters.set_param(
                "test", record.test or '',
                )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
