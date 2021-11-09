from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseBadRequest, \
    HttpResponseServerError
from django.shortcuts import render
from django.core import serializers
from django.forms.models import model_to_dict
from datetime import date, datetime
from django.db.models import Sum
from decimal import *
import json
import requests
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.forms import modelform_factory

from cashflow import dauth
from expenses import models

"""
Shows one user.
"""
@require_GET
@login_required
def get_user(request, username):
    try: user = models.User.objects.get_by_natural_key(username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {
            'exception': 'Användaren finns inte'
        })

    if not user.profile.may_be_viewed_by(request.user): return render(request, '403.html')

    return render(request, 'users/information.html', {
        'showuser': user,
        'total': models.ExpensePart.objects.filter(expense__owner=user.profile).aggregate(Sum('amount'))
    })
    
"""
Shows one user's receipts.
"""
@require_GET
@login_required
def get_user_receipts(request, username):
    try: user = models.User.objects.get_by_natural_key(username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {
            'exception': 'Användaren finns inte'
        })

    if not user.profile.may_be_viewed_by(request.user): return render(request, '403.html')

    non_attested_expenses = []
    attested_expenses = []

    for expense in user.profile.expense_set.all():
        if expense.reimbursement is not None: continue  # expense is waay past attesting

        for expense_part in expense.expensepart_set.all():
            if expense_part.attested_by is None:
                non_attested_expenses.append(expense)
                break
        else: attested_expenses.append(expense) # inner loop didn't break

    non_attested_expenses.sort(key=(lambda exp: exp.id), reverse=True)
    attested_expenses.sort(key=(lambda exp: exp.id), reverse=True)

    return render(request, 'users/receipts.html', {
        'showuser': user,
        'non_attested_expenses': non_attested_expenses,
        'attested_expenses': attested_expenses,
        'reimbursements': user.profile.receiver.all()
    })

"""
Shows edit user form and handles its request.
"""
@require_http_methods(["GET", "POST"])
@login_required
def edit_user(request, username):
    # noinspection PyPep8Naming
    UserForm = modelform_factory(models.Profile, fields=('bank_account', 'sorting_number', 'bank_name', 'default_account'))
    try: user = models.User.objects.get_by_natural_key(username)
    except ObjectDoesNotExist:
        return render(request, '404.html', {
            'exception': 'Användaren finns inte'
        })

    if username != request.user.username:
        return render(request, '403.html')

    if request.method == 'POST':
        received_form = UserForm(request.POST, instance=user.profile)
        if received_form.is_valid():
            received_form.save()
            return HttpResponseRedirect(reverse('user-show', args=[username]))

    form = UserForm(instance=user.profile)
    return render(request, 'users/edit.html', {
        'form': form,
        'showuser': user,
        'hide_edit': True
    })

