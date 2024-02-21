from setuptools import setup

setup(name='bot_assistant',
      version='1.0.0',
      description='Bot for addressbook and notes creation and usage',
      url='https://github.com/Yuliia-Vogel/team-project1-group10',
      author='Group 10 named team "πT\они", Python-core21, GoIT, 20 Feb 2024',
      author_email='arwen.vogel@gmail.com',
      license='MIT',
      packages=['bot_assistant'],
      install_requires=['prompt_toolkit>=3.0.43'],
      include_package_data=True,
      entry_points = {
          'console_scripts': [
              'otto = bot_assistant.main:main'
          ]
      }
      )