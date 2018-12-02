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

    #初始化标签列
    lab_col = 0

    #根据第7列的值来选择标签
    ex_col = 6

    #用于判断是否是第一行
    line_cnt = 0

    #实验列集合
    ex_list = []

    #标签列集合
    lab_list = []

    #输入数据每一行
    line_list = []

    #1、最后一列为标签列
    #2、获得ex_list
    #3、获得lab_list
    #4、获得line_list
    #5、对lab_list和ex_list 去重排序
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

    #1、实验列，找到每个元素在这一列里字典序去重排序以后的位置
    #比如 1、3、2、2 -> ex_list = 1，2，3 -> ex_dict = {1->0, 3->2, 2->1, 2->1}
    ex_dict = dict()
    for line in range(len(ex_list)):
        ex_dict[ex_list[line]] = line

    #比如 ex_list = {7,8,9,10,11}, lab_list = {0,1,2,3}
    #len(ex_list) = 5, len(lab_list) = 4
    #按照 5/4=1的长度来分割lab_list 7,8,9,10 11 -> 0,1,2,3 3
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
        if(index >= len(lab_list)):
            index = len(lab_list) - 1
        line[lab_col] = lab_list[index]
        cc_index = 0
        for cc in line:
            if cc_index == 0:
                result = result + cc
                cc_index += 1
            else:
                result += ',' + cc
        result += '\n'
    return result
