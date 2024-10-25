# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
{
    'name': 'Barge Load',
    'author': 'Lisivka Sergii',
    'category': 'Customizations',
    'summary': 'Barge Load',
    'website': 'https://odoo.school/',
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        # 'security/hr_hospital_group.xml',
        # 'security/hr_hospital_security.xml',
        'security/ir.model.access.csv',
        'views/barge_load_captain_views.xml',
        'views/barge_load_barge_views.xml',
        # 'reports/hr_hospital_doctor_report.xml',
        # 'views/hr_hospital_doctor_views.xml',
        # 'views/hr_hospital_disease_views.xml',
        # 'views/hr_hospital_diagnosis.xml',
        # 'views/hr_hospital_visit_views.xml',
        #
        # 'wizards/mass_update_doctor_wizard_views.xml',
        # 'wizards/report_diagnosis_wizard_view.xml',
        'views/barge_load_menu.xml',  # Завантажується останнім
    ],

    'demo': [
        # 'demo/hr.hospital.disease.csv',
        # 'demo/hr.hospital.doctor.csv',
        # 'demo/hr.hospital.patient.csv',
        # 'demo/hr_hospital_demo.xml',  # Завантажується останнім
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
