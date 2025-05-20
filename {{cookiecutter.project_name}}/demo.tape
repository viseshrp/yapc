Set Shell bash
Set FontSize 18
Set Width 800
Set Height 600
Output demo.gif

Hide Sleep 2s Show

Hide
Type "clear"
Enter
Show

{% if cookiecutter.cli_tool == "y" -%}
# CLI demo
Type "{{cookiecutter.project_slug}} --help"
Sleep 2s
Enter
Sleep 6s
{% else %}
# Python library demo
Type "python"
Sleep 3s
Enter

Type "import {{cookiecutter.project_slug}}"
Sleep 2s
Enter
# Pause for dramatic effect...
Sleep 4s

Type "help({{cookiecutter.project_slug}})"
Sleep 2s
Enter
Sleep 6s

Type "{{cookiecutter.project_slug}}.__version__"
Sleep 2s
Enter
Sleep 4s

Type "exit()"
Sleep 2s
Enter
Sleep 4s
{%- endif %}

Hide
Type "clear"
Enter
Show
