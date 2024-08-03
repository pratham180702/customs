
{
    'name': 'PK Hospital',
    'version': '1.0',
    'summary': 'This is the test hospital module',
    'license': 'LGPL-3',
    'data': [
        'security/groups.xml',
        'security/rec_rules_test.xml',
        'security/ir.model.access.csv',
        'wizard/change_health_status.xml',
        'wizard/calculate_bmi.xml',
        'views/hobby.xml',
        'views/drugs.xml',
        'views/partner_phone_exists.xml',
        'views/patient_view.xml',
        'views/hospital.xml',
        'views/doctors.xml',
        'views/diseases.xml',
        'views/menu.xml',
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    'depends': ['base','mail'],
    'application':'True',
    'sequence':'1'
}
