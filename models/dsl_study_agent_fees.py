# -*- coding: utf-8 -*-
from odoo import api, fields, models

class DslStudyAgentFees(models.Model):
    _name = 'dsl.study.agent.fees'
    _description = 'Agent Fees'
    _rec_name = 'agent_id'
    _order = 'id desc'

    agent_id = fields.Many2one('dsl.study.agent', string='Agent', required=True, ondelete='cascade')
    payment_date = fields.Date(string='Payment Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('other', 'Other'),
    ], string='Payment Method', default='cash')
    notes = fields.Text(string='Notes')
