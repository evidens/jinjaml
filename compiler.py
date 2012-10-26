#!/usr/bin/env python

import codecs
import yaml
import re
from jinja2 import Environment, FileSystemLoader

def main(conf_name=None, template_name=None, template_dir='.'):
    conf = load_conf(conf_name)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    return template.render(conf)

def load_conf(conf_name=None):
    """Loads the configuration file and replaces variables defined in the collection"""
    with codecs.open(conf_name, encoding='utf-8') as f:
        conf = yaml.load(f)

    # Replace variable substititions
    var_finder = re.compile(r'\$\{(\w+)\}')
    for k, v in conf.items():
        m = var_finder.search(v)
        if m:
            replace = conf[m.group(1)]
            conf[k] = var_finder.sub(replace, v)

    return conf

def init_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Feeds a yaml config file into a jinja2 template")
    parser.add_argument('conf_name', type=str, help="Path to the configuration file to load")
    parser.add_argument('template_name', type=str, help="Template file to render into")
    parser.add_argument('-t', '--template-dir', type=str,
                        help="""Directory where templates are stored (assumes dir from which script is run)""",
                        default='.')
    parser.add_argument('-o', '--output', type=str, help="Output file")


    return parser

if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()

    rendered = main(args.conf_name, args.template_name, args.template_dir)
    if args.output:
        with codecs.open(args.output, 'w', encoding='utf-8') as o:
            o.write(rendered)
    else:
        print rendered
