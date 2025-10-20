from odoo import models, fields, api
import pytz
class DslStudyFollowUp(models.Model):
    _name = 'dsl.study.follow.up'
    _description = 'DSL Study Follow Up'


    active = fields.Boolean(string="Active", default=True)
    schedule_date = fields.Datetime(string="Date", required=True)
    lead_id = fields.Many2one('crm.lead', string="Lead", required=True)
    note = fields.Text(string="Note")
    activity_type = fields.Selection(
        [('call', 'Call'), ('meeting', 'Meeting'), ('email', 'Email')],
        string='Activity Type'
    )

    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active  

        #  Schedule Activity 
    @api.model
    def create(self, vals):
        record = super(DslStudyFollowUp, self).create(vals)

        if record.schedule_date and record.lead_id:
            activity_type = self.env.ref('mail.mail_activity_data_todo')

            model_id = self.env['ir.model']._get('crm.lead').id

            self.env['mail.activity'].create({
                'res_model_id': model_id,               
                'res_id': record.lead_id.id,            
                'user_id': record.lead_id.user_id.id or self.env.uid,
                'date_deadline': record.schedule_date,
                'summary': record.note or 'Follow Up',
            })

            record.lead_id.message_post(
                body=f"Follow-up scheduled for {record.schedule_date}.\n{record.note or ''}",
                message_type='notification'
            )

        return record

        
            