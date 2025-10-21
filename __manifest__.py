# -*- coding: utf-8 -*-
{
    'name': "DSL Study Core",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'website', 'web'],

    'assets': {
        'web.assets_frontend': [
            'dsl_study_core/static/src/css/style.css',
            'dsl_study_core/static/src/css/outfit.css',
            
        ],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',
        'data/strm_stages.xml',

        "views/dsl_study_student_view.xml",
        "views/dsl_study_parent_view.xml",
        "views/dsl_study_address_view.xml",
        "views/dsl_study_sponsor_view.xml",
        "views/education_board_view.xml",
        "views/dsl_study_result_view.xml",
        "views/dsl_study_document_type_view.xml",
        'views/dsl_study_student_program_line_view.xml',
        'views/dsl_study_agent_view.xml',
        'views/dsl_study_agent_fees_view.xml',

        'views/crm_views.xml',
        'views/dsl_study_country_views.xml',
        'views/dsl_study_country_institute_views.xml',
        'views/dsl_study_country_institute_program_views.xml',
        'views/dsl_study_source_views.xml',
        'views/dsl_study_follow_up.xml',
        'views/strm_views.xml',
        'views/strm_stages_view.xml',
        'views/student_profile_form.xml',
        'views/portal_template.xml',
        # 'views/user_dashboard.xml',
        'views/admission_ac_header.xml',

        "wizard/security_money_wizard_view.xml",
        "wizard/document_charge_wizard_view.xml",

        'views/menu.xml',
    ],

}

