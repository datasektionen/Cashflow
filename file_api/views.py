from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date, datetime
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from pi_heif import register_heif_opener
from io import BytesIO

import re

from expenses.models import File
from expenses.models import Expense

register_heif_opener()

def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        #'{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        #body=request.body,
    )


@require_http_methods(["POST"])
@csrf_exempt
def new_file(request):
    if len((request.FILES.getlist('files'))) < 1:
        return JsonResponse({'message':'No file specified.','explanation':'Upload at least one file.'}, status=400)

    eId = int(request.GET.get('expense', '0'))
    expense = None
    if eId > 0:
        expense = Expense.objects.get(pk=eId)
        expense.confirmed_by = None
        expense.confirmed_at = None
        expense.save()

    # Upload the file
    files = []
    for uploaded_file in request.FILES.getlist('files'):
        if uploaded_file.content_type == 'image/heif':
            img = BytesIO()
            with Image.open(uploaded_file) as im:
                im.save(img, format="jpeg")
            uploaded_file = InMemoryUploadedFile(
                img,
                None,
                uploaded_file.name.lower().replace(".heic", ".jpeg"),
                "image/jpeg",
                img.getbuffer().nbytes,
                "binary"
            )

        file = File(file=uploaded_file, expense=expense)
        file.save()

        files.append(file)

    return JsonResponse({'message':'File uploaded.', 'files':[file.to_dict() for file in files]})

@require_http_methods(["POST"])
@csrf_exempt
def delete_file(request, pk):
    file = File.objects.get(pk=int(pk))
    if not file.expense == None and not request.user.profile.may_delete(file.expense):
        return JsonResponse({'Du har inte behörighet att ta bort denna bild.'}, 403)
    file.expense.confirmed_by = None
    file.expense.confirmed_at = None
    file.expense = None
    file.save()

    return JsonResponse({'message':'File deleted.'})
