from setuptools import setup, find_packages
setup(
   name='key-proxy',
   version='1.0.1',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   python_requires='>=3.7',
   py_modules = ['script', 'src'],
   entry_points='''
      [console_scripts]
      key-proxy=script:hello
      ''',
)