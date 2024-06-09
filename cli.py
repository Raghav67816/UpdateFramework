# UNDER DEVELOPMENT

from json import loads

# define parser
arg_parser = argparse.ArgumentParser(
    prog="Updater Framework",
    description="Update your application flawlessly."
)
arg_parser.add_argument('-e', '--endpoint')
arg_parser.add_argument('-p', '--products')
arg_parser.parse_args()
