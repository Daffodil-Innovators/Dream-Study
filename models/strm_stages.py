# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StrmStages(models.Model):
    _inherit = 'crm.stage'
    _description = 'STRM Stages'

    is_strm = fields.Boolean(string="Is STRM", default=False)
    is_won = fields.Boolean('Is Won Stage?')
    state = fields.Selection(
            [   ("new", "New"),
                ("office_visit", "Office Visit"),
                ("file_open", "File Open"),
                ("inprogress", "In Progress"),
                ("re_draft", "Re Draft"),
                ("won", "Won"),
                ("not_interested", "Not Interested"),
            ],
            string="Status",
            default="office_visit",
            tracking=True,
        )