
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import io as StringIO
import cgi
import os


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), dest=result,link_callback=fetch_resources,encoding="utf-8")
    pdf= pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result,link_callback=fetch_resources)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result,link_callback=fetch_resources, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path
