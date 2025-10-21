from odoo import http
from odoo.http import request
import base64

class DslStudentPortalController(http.Controller):

    @http.route('/my/profile', type='http', auth='user', website=True)
    def my_profile_form(self, **kw):
        """Display the student registration/profile form for the logged-in user"""
        user = request.env.user
        student = request.env['dsl.study.student'].sudo().search([('partner_id', '=', user.partner_id.id)], limit=1)
        countries = request.env['res.country'].sudo().search([])
        officers = request.env['res.users'].sudo().search([])

        return request.render('dsl_study_core.student_profile_form', {
            'student': student,
            'countries': countries,
            'officers': officers,
        })
        
    @http.route(['/my/profile'], type='http', auth='user', website=True)
    def my_profile(self, **kw):
        student = request.env['dsl.study.student'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)], limit=1)
        countries = request.env['res.country'].sudo().search([])
        officers = request.env['res.users'].sudo().search([])
        return request.render('dsl_study_core.student_profile_form', {
            'student': student,
            'countries': countries,
            'officers': officers,
            'page_name': 'my_profile',  # important for breadcrumb
        })
    

    @http.route('/my/profile/submit', type='http', auth='user', website=True, methods=['POST'])
    def my_profile_submit(self, **post):
        """Save or update student profile for logged-in user"""
        user = request.env.user
        student_model = request.env['dsl.study.student'].sudo()
        student = student_model.search([('partner_id', '=', user.partner_id.id)], limit=1)

        photo_file = request.httprequest.files.get('photo')
        photo_data = False
        if photo_file:
            photo_data = base64.b64encode(photo_file.read())

        vals = {
            'first_name': post.get('first_name'),
            'middle_name': post.get('middle_name'),
            'last_name': post.get('last_name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'photo': photo_data or (student.photo if student else False),
            'country': int(post.get('country')) if post.get('country') else False,
            'note': post.get('address'),
            'admission_officer_ids': [(6, 0, [int(post.get('officer'))])] if post.get('officer') else False,
            'partner_id': user.partner_id.id,
        }

        if student:
            student.write(vals)
        else:
            student_model.create(vals)

        return request.redirect('/my/profile?success=1')
