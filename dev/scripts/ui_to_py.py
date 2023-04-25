import os

uis = [
    'MainWindow',
    'ConfigurationDialog',
    'SupplierDialog',
    'YearDialog',
    'CalendarDialog',
    'ImportBackupDialog'
]

for ui in uis:
    os.system(fr'pyuic6 -x .\ui\{ui}.ui -o .\ui\{ui}.py')
