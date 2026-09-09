{
    "name": "Hospital Management",
    "version": "1.0.0",
    "summary": "Hospital custom Modules",
    "author": "A. M. W. K.",
    "license": "LGPL-3",
    "sequence": -100,
    "category": "Custom",
    "depends": ["base","mail","product","sale","sale_stock"],
    "data": [
        "security/ir.model.access.csv",
        "data/patient_data.xml",
        'data/appointment_server_action.xml',
        "data/hospital.patient.csv",
        "data/patient_sequence.xml",
        "views/sale_order_views.xml",
        "views/hospital_patient_views.xml",
        "views/hospital_patient_female_views.xml",
        
        "views/appointment_cancel_wizard_views.xml",
        "views/hospital_appointment_views.xml",
        "views/hospital_patient_tag_views.xml",
         "views/menu.xml",
        "views/hospital_operation_views.xml",
       
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
    "assets": {
        'web.assets_backend': [
            'hospital/static/src/css/hospital.css',
        ],
    },
    
}  # type: ignore
