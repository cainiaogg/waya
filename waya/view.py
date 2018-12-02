from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from waya.models import Data
import os
# Create your views here.

filename = '/Users/joseph/work/python/poem.txt'

class DataForm(forms.Form):
    datatype = forms.CharField()
    database = forms.FileField()

def trans(request):
    if request.method == "POST":
        uf = DataForm(request.POST,request.FILES)
        if uf.is_valid():
            datatype = uf.cleaned_data['datatype']
            database = uf.cleaned_data['database']
            dir_name = "./upload/%s" % (database)
            if not os.path.exists(dir_name):
                os.system(r"touch {}".format(dir_name))
            f = open(dir_name, "w")
            for line in database:
                f.write(line)
            f.close()
            if(datatype == 'text'):
                return HttpResponse(deal_text(dir_name))
            return HttpResponse('upload ok!')
    else:
        uf = DataForm()
    return render_to_response('trans.html',{'uf':uf})

def deal_text(dir_name):
    f = open(dir_name, 'r')
    lab_col = 0
    ex_col = 6
    line_cnt = 0
    ex_list = []
    lab_list = []
    line_list = []

    for line in f.readlines():
        line_list.append(line)
        try:
            line = line.strip().split(',')
            if(line_cnt == 0):
                line_cnt += 1;
                lab_col = len(line) - 1
                continue
            ex_list.append(line[ex_col])
            lab_list.append(line[lab_col])
        except Exception:
            pass
    lab_list = list(set(lab_list))
    lab_list.sort()
    ex_list = list(set(ex_list))
    ex_list.sort()
    f.close()

    ex_dict = dict()
    for line in range(len(ex_list)):
        ex_dict[ex_list[line]] = line

    line_cnt = 0
    result = ""
    for line in line_list:
        if(line_cnt==0):
            result += line
            line_cnt = 1
            continue
        line = line.strip().split(',')
        index = ex_dict[line[ex_col]]
        index = index / (len(ex_list)/len(lab_list))
        line[lab_col] = lab_list[index - 1]
        cc_index = 0
        for cc in line:
            if cc_index == 0:
                result = result + cc
                cc_index += 1
            else:
                result += ',' + cc
        result += '\n'
    return result
