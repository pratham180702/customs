# -*- coding: utf-8 -*-
{
    'name': "Patient Report",
    'summary': "Patient Report Template",
    'description': """
        Patient report
    """,
    'license': 'LGPL-3',
    # 'author': "Imad Bourouche",
    # 'email': "ji_bourouche@esi.dz",
    # 'category': 'Administration',
    'version': '0.1',
    'application': True,
    'depends': ['pk_hospital'],
    'data': [
        'report/patient_report_template.xml',
    ],
}