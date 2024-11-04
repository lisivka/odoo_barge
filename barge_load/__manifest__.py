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
        'security/ir.model.access.csv',
        'views/barge_load_quarry_views.xml',
        'views/barge_load_barge_views.xml',
        'views/barge_load_dredger_views.xml',
        'views/barge_load_tugboat_views.xml',
        'views/barge_load_act_views.xml',

        'wizards/mass_update_doctor_wizard_views.xml',

        'views/barge_load_menu.xml',  # Завантажується останнім
    ],

    'demo': [

        "demo/barge_load_demo.xml",
        "demo/barge_load_demo_act.xml"
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
