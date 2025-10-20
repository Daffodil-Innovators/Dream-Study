# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SecurityMoneyWizard(models.TransientModel):
    _name = 'security.money.wizard'
    _description = 'Security Money Wizard'

    student_id = fields.Many2one('dsl.study.student', string='Student', required=True)
    amount = fields.Float(string='Security Amount', required=True)

    def action_confirm_payment(self):
        self.ensure_one()
        if self.amount <= 0:
            raise UserError(_("Amount must be greater than zero."))

        student = self.student_id

        if not student.partner_id:
            raise UserError(_("Student must have a linked partner to register payment."))

        payment_vals = {
            "partner_id": student.partner_id.id,
            "amount": self.amount,
            "payment_type": "inbound",
            "partner_type": "customer",
        }

        payment = self.env["account.payment"].create(payment_vals)
        student.security_money_done = True

        return {
            "type": "ir.actions.act_window",
            "name": "Security Payment",
            "res_model": "account.payment",
            "view_mode": "form",
            "res_id": payment.id,
            "target": "current",
        }
