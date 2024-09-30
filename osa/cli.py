# cli.py

import os
import click
from wsgiref.simple_server import make_server
import importlib
import sys

class NoAppException(click.UsageError):
    """Raised if an application cannot be found or loaded."""

"""
1 - 
used to dynamically load a Python module from a file path.
Here's a detailed explanation and some examples:
importlib.util.spec_from_file_location:

This function creates a module specification (ModuleSpec) from a file location.
It is part of the importlib.util module, which provides utilities for the import system.
Arguments:
    name: The name of the module.
    location: The file path to the module.
    module_name:
This is a variable that holds the name of the module you want to load.
It should be a string representing the module's name.
os.path.join(os.getcwd(), f"{module_name}.py"):

This constructs the file path to the module.
os.getcwd():
    This function returns the current working directory as a string.
f"{module_name}.py":
    This is an f-string that creates the filename by appending .py to the module name.
os.path.join:
This function joins one or more path components intelligently. It returns a string representing the full path to the module file.
Functions

importlib.util.spec_from_file_location:
Purpose: To create a ModuleSpec object from a file location.
Usage: This is used when you need to load a module dynamically from a specific file path.
Returns: A ModuleSpec object that can be used to create and load the module.

os.getcwd():
Purpose: To get the current working directory.
Usage: This is used to construct the full path to the module file.
Returns: A string representing the current working directory.

os.path.join:
Purpose: To join one or more path components intelligently.
Usage: This is used to construct the full path to the module file by joining the current working directory and the module filename.
Returns: A string representing the full path to the module file.
"""

def find_app_module(app_argument=None):
    """
    Finds and imports the app module.
    Supports setting the module and app name via the command-line argument
    or via the OSA_APP environment variable (similar to Flask's behavior).
    """
    app_module_name = None
    app_variable_name = "app"  # Default variable name is 'app'

    # Step 1: Check if the app is passed via command-line argument (like --app module_name:app_name)
    if app_argument:
        if ":" in app_argument:
            app_module_name, app_variable_name = app_argument.split(":")
        else:
            app_module_name = app_argument
    else:
        # Step 2: Check the OSA_APP environment variable
        app_module_name = os.getenv('OSA_APP', None)
        if app_module_name and ":" in app_module_name:
            app_module_name, app_variable_name = app_module_name.split(":")
    
    if not app_module_name:
        # Step 3: Try to load from the current working directory
        # Dynamically try to load the app from 'wsgi.py' or 'app.py'
        # Source : https://www.pythonmorsels.com/dynamically-importing-modules/
        possible_modules = ('app', 'wsgi')
        for module_name in possible_modules:
            try:
                # 1
                spec = importlib.util.spec_from_file_location( 
                    module_name, os.path.join(os.getcwd(), f"{module_name}.py")
                )
                if spec:
                    app_module = importlib.util.module_from_spec(spec) # Create a module from spec
                    spec.loader.exec_module(app_module) # Execute the module
                    app = getattr(app_module, app_variable_name, None)  # Get app_variable_name from module
                    if app:
                        return app
                    raise NoAppException(
                    f"Could not locate an app named '{app_variable_name}' in module '{module_name}'."
                )
            except FileNotFoundError:
                continue
    else:
        # Step 4: Load the specified module and app
        spec = importlib.util.spec_from_file_location(
            app_module_name,
            os.path.join(os.getcwd(), f"{app_module_name}.py")
            )
        if spec:
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            app = getattr(app_module, app_variable_name, None)
            if app:
                return app
            raise NoAppException(
                f"Could not locate an app named '{app_variable_name}' in module '{app_module_name}'."
            )
    raise NoAppException(
                "Could not locate a osa application. Use the"
                " 'osa --app' option, 'OSA_APP' environment"
                " variable, or a 'wsgi.py' or 'app.py' file in the"
                " current directory."
            )


@click.group()
def cli():
    """Command-line interface for the Osa web framework.
    osa run --app=filename:application_name """
    pass

@click.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the server to.')
@click.option('--port', default=8300, help='Port to run the server on.')
@click.option('--app' ,help='The WSGI application to run,e.g,->filename:application_name.', required=False)
@click.option('--no-debug', is_flag=True, help='Disable debug mode.')
def run(host, port,app=None, no_debug=False):
    """Run the web server."""
    app = find_app_module(app)
    
    if app is None :
        raise  NoAppException("Unable to find a valid Osa app instance in the current directory.")
    if not callable(app):
        raise NoAppException("The app is not a valid WSGI application.")
    if no_debug:
        app.debug = False
    click.secho(f"WARNING: This is a simple development server. Do not use it in a production deployment.",fg='red')
    click.secho(f"Use a production WSGI server instead.")

    with make_server(host, port, app) as httpd:
        click.secho(f" * Running on http://{host}:{port}/ (Press CTRL+C to quit)",fg='green')
        httpd.serve_forever()

# Add the run command to the CLI group
cli.add_command(run)
def main():
    cli()

