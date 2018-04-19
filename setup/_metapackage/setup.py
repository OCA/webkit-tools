import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-webkit-tools",
    description="Meta package for oca-webkit-tools Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-base_headers_webkit',
        'odoo8-addon-report_webkit_barcode',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
