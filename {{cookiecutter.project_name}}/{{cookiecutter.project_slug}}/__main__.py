{{ ("The main entry point for the " ~ cookiecutter.project_name ~ " package.")|tojson }}

from .cli import main

if __name__ == "__main__":
    main()
