from pathlib import Path
import random
from subprocess import run

from jinja2 import Environment, FileSystemLoader
import requests


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


def get_apple_pdf():
    if Path("apple.pdf").exists():
        return
    url = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/svg/"
    file_name = "emoji_u1f34e.svg"
    svg_text = requests.get(url + file_name).text
    with open("apple.svg", "w", encoding="utf-8") as f:
        f.write(svg_text)
    run([
        "inkscape",
        "--export-type=pdf",
        "apple.svg"
    ])
    Path("apple.svg").unlink()



def render_latex_template(template_name: str):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    apple_count = random.randint(2, 10)
    context = {
        "a": f"{a}",
        "b": f"{b}",
        "result": f"{a + b}",
        "apple_count": f"{apple_count}",
        "apples": apple_count * r"\scalerel*{\includegraphics{apple}}{A}",
    }
    with open(template_name + ".tex", "w", encoding="utf-8") as f:
        f.write(render_template("template", context))


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
    print("Getting apple PDF...")
    get_apple_pdf()
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
