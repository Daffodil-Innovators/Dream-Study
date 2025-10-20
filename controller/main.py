from odoo import http
from odoo.http import request
import base64


class DslStudentPortalController(http.Controller):

    @http.route('/my/home/dashboard', type='http', auth='user', website=True)
    def student_dashboard(self, **kw):
        """
        Display the student dashboard with only 'My Payments' card.
        """
        user = request.env.user

        # Safely find the student record linked to this user
        student = request.env['dsl.study.student'].sudo().search([
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)

        # Count invoices linked to student's partner
        invoice_count = 0
        if student and student.partner_id:
            invoice_count = request.env['account.move'].sudo().search_count([
                ('move_type', '=', 'out_invoice'),
                ('partner_id', '=', student.partner_id.id)
            ])

        values = {
            'user_id': user,
            'student_profile': student,
            'student_invoices': invoice_count,
            'page_name': 'student_dashboard',
        }

        return request.render('dsl_study_core.user_dashboard_admission_ac', values)


    @http.route('/my/home/dashboard/submit', type='http', auth='user', website=True, methods=['POST'])
    def student_dashboard_submit(self, **post):
        """
        Save or update the student profile from the dashboard form.
        """
        user = request.env.user
        student_model = request.env['dsl.study.student'].sudo()
        student = student_model.search([
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)

        # Handle uploaded photo
        photo_file = request.httprequest.files.get('photo')
        photo_data = False
        if photo_file:
            photo_data = base64.b64encode(photo_file.read())

        vals = {
            'first_name': post.get('first_name'),
            'middle_name': post.get('middle_name'),
            'last_name': post.get('last_name'),
            'gender': post.get('gender'),
            'date_of_birth': post.get('date_of_birth'),
            'nationality': post.get('nationality'),
            'blood_group': post.get('blood_group'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'photo': photo_data or (student.photo if student else False),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'zip': post.get('zip'),
            'state_id': int(post.get('state')) if post.get('state') else False,
            'country_id': int(post.get('country')) if post.get('country') else False,
            'note': post.get('address'),
            'admission_officer_ids': [(6, 0, [int(post.get('officer'))])] if post.get('officer') else False,
            'partner_id': user.partner_id.id,
        }

        if student:
            student.write(vals)
            if student.state == 'draft':
                student.state = 'submitted'
        else:
            vals['state'] = 'submitted'
            student_model.create(vals)

        return request.redirect('/my/dashboard?success=1')
