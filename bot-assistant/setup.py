from setuptools import setup

setup (name='bot-assistant',
      version='1.0.0',
      description='Bot for addressbook and notes creation and usage',
      url='https://github.com/Yuliia-Vogel/team-project1-group10',
      author='Group 10 named team "πT\они", Python-core21, GoIT, 20 Feb 2024',
      author_email='arwen.vogel@gmail.com'
      license='MIT',
      packages=['bot-assistant'],
      install_requires=[], #? pip - дописати, коли перегляну лекцію
      entry_points={'console_scripts': ['bot-assistant = bot-assistant.main:main']})