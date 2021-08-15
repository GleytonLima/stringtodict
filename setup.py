from setuptools import setup

setup(
    name='stringtodict',
    version='0.0.2',
    author='Gleyton Lima',
    author_email='gleytonclima@gmail.com',
    packages=['stringtodict'],
    description='Um simples conversor de texto em dicionário e de dicionário em texto',
    long_description='Um conversor de texto que serializa uma string para dicionário e dicionário para texto',
    url='https://github.com/GleytonLima/stringtodict',
    project_urls={
        'Código fonte': 'https://github.com/GleytonLima/stringtodict'
    },
    license='MIT',
    keywords='conversor string dicionário json parser',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here
        'Programming Language :: Python :: 3',
    ]
)
