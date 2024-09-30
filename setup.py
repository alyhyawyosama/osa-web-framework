from setuptools import setup, find_packages

setup(
    name='osa-web-framework',  
    version='0.0.1',
    description='A simple web framework for Python developers to learn how some fundamental concepts of web frameworks work under the hood.',  
    author='Alyahyawy Osama',
    author_email='alyhyawyosama@gmail.com',
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        'click',        # For command-line interface
        'webob',        # For request and response objects
        'requests',     # For the test client
        'parse',        # For URL parsing
        'requests-wsgi-adapter',  # For integrating with WSGI in the test client,
        'whitenoise',   # For serving static files
        'jinja2',       # For rendering templates

    ],
    entry_points={
        'console_scripts': [
            'osa=osa.cli:main',  # Expose the CLI command
        ],
    },
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
