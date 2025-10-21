from odoo import api, fields, models

class DslStudyStudentProgramLine(models.Model):
    _name = 'dsl.study.student.program.line'
    _description = 'Student Program Line'
    _rec_name = 'program_id'



    student_id = fields.Many2one(
        'dsl.study.student',
        string='Student',
        ondelete='cascade'
    )

    country_id = fields.Many2one(
        'dsl.study.country',
        string='Country',
        help='Preferred country (defaulted from student if available)'
    )

    institute_id = fields.Many2one(
        'dsl.study.country.institute',
        string='Institute',
        help='Preferred institute (defaulted from student if available)'
    )

    program_id = fields.Many2one(
        'dsl.study.country.institute.program',
        string='Program'
    )

    is_student_agree = fields.Boolean(
        string='Student Agreed',
        default=False
    )

    # common
    note = fields.Text(string="Notes")
    code = fields.Char(string="Code", default="New", readonly=True, copy=False)
    active = fields.Boolean(default=True)


    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('confirmed', 'Confirmed'),
        ('applied', 'Applied'),
        ('offer_letter', 'Offer Letter'),
        ('sponsor_and_document', 'Sponsor & Document'),
        ('tuition_fee', 'Tuition Fee'),
        ('visa_processing', 'Visa Processing'),
        ('file_handover', 'File Handover'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)


    apply_state = fields.Selection(
        [('submit', 'Submit'),
         ('pending', 'Pending')],
        string='Apply State',
        default='pending'
    )

    offer_letter_state = fields.Selection(
        [('issued', 'Issued'),
         ('accepted', 'Accepted'),
         ('rejected', 'Rejected')],
        string='Offer Letter State',
        default='issued'
    )

    tuition_fee_state = fields.Selection(
        [('paid', 'Paid'),
         ('unpaid', 'Unpaid')],
        string='Tuition Fee State',
        default='unpaid'
    )

    final_offer_state = fields.Selection(
        [('received', 'Received'),
         ('not_received', 'Not Received')],
        string='Final Offer State',
        default='not_received'
    )

    # -- STATE ACTIONS --------------------------------------------------------
    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_applied(self):
        for rec in self:
            rec.state = 'applied'

    def action_offer_letter(self):
        for rec in self:
            rec.state = 'offer_letter'

    def action_sponsor_documents(self):
        for rec in self:
            rec.state = 'sponsor_and_document'

    def action_tuition_fee(self):
        for rec in self:
            rec.state = 'tuition_fee'

    def action_visa_processing(self):
        for rec in self:
            rec.state = 'visa_processing'
    def action_file_handover(self):
        for rec in self:
            rec.state = 'file_handover'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft' 

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = (
                self.env["ir.sequence"].next_by_code("dsl.study.student.program.line") or "New"
            )
        return super().create(vals)
