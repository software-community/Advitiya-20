from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import csv

from ca.models import Profile

# Create your views here.

@staff_member_required
def gen_ca_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ca_detail.csv"'

    writer = csv.writer(response)
    cas = Profile.objects.all()
    writer.writerow(['Name', 'College Name', 'Email', 'Mobile', 'Tech Head', 'Tech Head Phone', 'Past Exp', 'CA CODE'])
    for ca_user in cas:
        writer.writerow([ca_user.your_name, ca_user.college_name, ca_user.user.email, ca_user.phone,
                            ca_user.tec_head, ca_user.tec_head_phone, ca_user.past_exp, ca_user.ca_code ])

    return response