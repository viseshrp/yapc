Set Shell bash

Hide Sleep 2s Show

# Where should we write the GIF?
Output demo.gif

Set FontSize 18
Set Width 800
Set Height 600

Hide
Type "clear"
Enter
Show

# Type a command in the terminal.
# Activate virtual environment
Type "source .venv/bin/activate"
Sleep 1s
Enter
Sleep 1s

{% if cookiecutter.cli_tool == "y" %}
# CLI demo
Type "{{cookiecutter.project_slug}} --help"
Sleep 2s
Enter
Sleep 4s
{% else %}
# Python library demo
Type "python"
Sleep 2s
Enter

Type "import {{cookiecutter.project_slug}}"
Sleep 2s
Enter
# Pause for dramatic effect...
Sleep 4s

Type "help({{cookiecutter.project_slug}})"
Sleep 2s
Enter
Sleep 4s

Type "{{cookiecutter.project_slug}}.__version__"
Sleep 2s
Enter
Sleep 4s

Type "exit()"
Sleep 2s
Enter
Sleep 4s
{% endif %}

Hide
Type "clear"
Enter
Show
