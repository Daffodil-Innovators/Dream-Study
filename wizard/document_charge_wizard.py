# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class DocumentChargeWizard(models.TransientModel):
    _name = 'document.charge.wizard'
    _description = 'Document Charge Wizard'

    student_id = fields.Many2one('dsl.study.student', string='Student', required=True)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Char(string='Description', default='Document Charge')
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', '=', 'sale')])
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.context_today)

    def action_confirm(self):
        self.ensure_one()
        student = self.student_id
        if not student.partner_id:
            raise UserError(_("Student must have a linked partner to create an invoice."))

        # find a sale journal if not provided
        journal = self.journal_id or self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError(_("No sale journal is configured. Please set a Sales journal."))

        # find an income account for invoice line
        income_account = self.env['account.account'].search([('account_type', '=', 'income')], limit=1)
        if not income_account:
            raise UserError(_("No income account found. Please configure an income account."))

        invoice_vals = {
            'move_type': 'out_invoice',     # customer invoice
            'partner_id': student.partner_id.id,
            'journal_id': journal.id,
            'invoice_date': self.invoice_date,
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.description or 'Document Charge',
                    'quantity': 1.0,
                    'price_unit': self.amount,
                    'account_id': income_account.id,
                })
            ],
        }

        invoice = self.env['account.move'].create(invoice_vals)

        # link to student
        student.document_charge_id = invoice.id
        student.move_ids = [(4, invoice.id)]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }
