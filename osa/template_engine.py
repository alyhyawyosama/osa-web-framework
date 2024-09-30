# template_engine.py

from jinja2 import Environment, FileSystemLoader
import os

class TemplateEngine:
    def __init__(self, templates_dir):
        self.templates_dir = os.path.abspath(templates_dir)
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

    def render(self, template_name, context=None):
        if context is None:
            context = {}
        return self.env.get_template(template_name).render(**context)
