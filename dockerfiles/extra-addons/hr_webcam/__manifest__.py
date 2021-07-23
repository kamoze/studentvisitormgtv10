{
    'name': 'Capture employee picture with webcam',
    'version' : '1.1',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR WebCam
=========

Capture employee pictures with an attached web cam.
    """,
    'author': "Geotechnosoft",
    'website': 'http://geotechnosoft.com',
    'license': 'AGPL-3',
    'depends': [
        'hr',
        'web',
    ],
    'js': [
        'static/src/js/jquery.webcam.js',
        'static/src/js/hr_webcam.js',
    ],
    'css': [
        'static/src/css/hr_webcam.css',
    ],
    'qweb': [
        'static/src/xml/hr_webcam.xml',
    ],
    'data': [
        'hr_webcam_data.xml',
        'hr_webcam_view.xml',
    ],
    'installable': True,
    'active': False,
}
