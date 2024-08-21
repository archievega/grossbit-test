from jinja2 import Environment, FileSystemLoader
import pdfkit


env = Environment(loader=FileSystemLoader("./templates"))


def render_pdf_check(id: str, data: dict):
    template = env.get_template("check.html")
    html_out = template.render(data)
    pdfkit.from_string(html_out, f"./media/{id}.pdf")
