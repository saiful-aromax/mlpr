"""
These are utility functions crated by Aromax
"""
from django.shortcuts import render
from django.template import loader


def layout(
    request, template_name, context=None, content_type=None, status=None, using=None, IsReturnedToText=False
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(
        template_name, context, request, using=using)
    return render(request, 'layout.html', {"content": content})
    # return HttpResponse(content, content_type, status)
