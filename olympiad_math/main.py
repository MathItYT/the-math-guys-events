from pathlib import Path
from subprocess import run

from jinja2 import Environment, FileSystemLoader


def clean_up():
    for p in Path.cwd().glob("math_from_zero*"):
        if p.name == "math_from_zero.tex":
            continue
        p.unlink()


def get_latex_environment():
    return Environment(
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(Path.cwd())
    )


def render_template(template_name: str, context: dict[str, str]) -> str:
    env = get_latex_environment()
    template = env.get_template(template_name + ".tex")
    return template.render(context)



def render_latex_template(template_name: str):
    with open(template_name + ".tex", "w", encoding="utf-8") as f:
        f.write(render_template("template", {}))


def compile_tex(tex_file: str):
    with open("output.log", "w") as f:
        run([
            "latex",
            "--shell-escape",
            "-interaction=nonstopmode",
            tex_file
        ], stdout=f)


def convert_to_svg(dvi_file: str):
    with open("output.log", "a") as f:
        run([
            "dvisvgm",
            "--font-format=woff",
            "--bbox=papersize",
            "--zoom=-1",
            "-p 1,-",
            "--linkmark=none",
            dvi_file
        ], stdout=f)


def get_html_environment():
    return Environment(
        loader=FileSystemLoader(Path.cwd())
    )


def write_html(file_initial: str):
    svgs = list(Path.cwd().glob(f"{file_initial}-*.svg"))[:-1]
    svgs = [svg.name for svg in svgs]
    env = get_html_environment()
    template = env.get_template("template.html")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(template.render(svgs=svgs))


def main():
    print("Cleaning up...")
    clean_up()
    print("Done!")
    print("Rendering template...")
    render_latex_template("math_from_zero")
    print("Done!")
    print("Compiling LaTeX...")
    compile_tex("math_from_zero")
    print("Done!")
    print("Converting to SVG...")
    convert_to_svg("math_from_zero")
    print("Done!")
    print("Writing HTML...")
    write_html("math_from_zero")
    print("Done!")


if __name__ == "__main__":
    main()
