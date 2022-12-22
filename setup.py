import os, sys, inspect
from setuptools import setup, find_packages

setup(
    name='email-resender',
    version='0.3',
    description='Пересылка писем с определенных ящиков с определенными темами',
    author='bds89',
    author_email='bds89@mail.ru',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6',
        'exchangelib',
        'PyYAML',
        'pyshortcuts'
],
    entry_points = {
        'console_scripts': ['email-resender=emailresender.__main__:main',
                            'email-resender_shortcut=emailresender.__main__:create_shortcut'],
    },
    package_data={'emailresender': ['res/*.*']},
)

# setup(
#     name='email-resender',
#     version='0.3',
#     description='Пересылка писем с определенных ящиков с определенными темами',
#     author='bds89',
#     author_email='bds89@mail.ru',
#     # packages=['emailresender', 'emailresender.GUI', 'emailresender.mail', 'emailresender.services'],
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         'PyQt6',
#         'exchangelib',
#         'PyYAML',
#         'pyshortcuts'
# ],
#     py_modules = ['GUI', 'mail', 'services'],
#     entry_points = {
#         'console_scripts': ['email-resender=emailresender.__main__:main'],
#     }
# )


        # from pyshortcuts import make_shortcut
        # patch = self.get_script_dir()
        # make_shortcut(script='email-resender', name='Email Resender',
        #                         icon=patch+'/email-resender/res/icon_active.png',
        #                         terminal=False)