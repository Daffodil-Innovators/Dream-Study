# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class DslStudyStudentDocumentLine(models.Model):
    _name = 'dsl.study.student.document.line'
    _description = 'Student Document Line'

    # relation to Student
    student_id = fields.Many2one('dsl.study.student', string='Student', required=True)
    document_type_id = fields.Many2one('dsl.study.document.type', string='Document Type', required=True)
    strm_id = fields.Many2one('crm.lead', string='Lead', required=True)

    # fields
    state = fields.Selection(
        [('collected', 'Collected'), ('not_collected', 'Not Collected')],
        string='Status',
        default='not_collected'
    )
    active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Notes')
    date = fields.Date(string='Date', default=fields.Date.context_today)