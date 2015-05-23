from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import *
from django.views.generic import TemplateView


# Create your views here.

def get_type_list():
    type_tuple = Dish.objects.values_list('typ').distinct()
    type_list = [] #reduce(lambda x,y:x + y, map(list,type_tuple))
    return type_list

def admin_check(user):
    try:
        if(user.myuser.perm == 2):
            return ture;
    except:
        pass
    return false; 

class logout(TemplateView):
    def get(self,req):
        auth.logout(req)
        return HttpResponseRedirect('/')

class login(TemplateView):
    template_name = "login.html"

    response=['','manager.html','clerk.html','chef.html']

    def get(self,req):
        if(req.user.is_authenticated()):
            return HttpResponseRedirect('/')
        state = ''
        content={'state':state,}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        
    def post(self,req):
        username = req.POST.get('username','')
        password = req.POST.get('password','')
        user = auth.authenticate(username = username,password = password)
        if(user is None):
            state = 'login_error'
            content={'state':state,}
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        else:
            auth.login(req,user)
            return HttpResponseRedirect(self.response[user.perm])

class index(TemplateView):
    template_name = "index.html"

    def get(self,req):
       # self.typ = req.GET.get('typ','recommend')
        self.typ = 'recommend'
        self.dish_list = Dish.objects.filter(typ = self.typ)
        self.page_num = 1
        self.main(req)

    def post(self,req):
        keywords = req.POST.get('keywords','')
        self.dish_list = Dish.objects.filter(name__contains = keywords)
        self.page_num = req.POST.get('page_num','')
        self.main(req)
        self.typ = 'all'

    def main(self,req):
        type_list = get_type_list()
        paginator = Paginator(self.dish_list,12) 
        try:
            show_list = paginator.page(self.page_num)
        except (PageNotAnInteger or EmptyPage):
            show_list = paginator.page(1)
        content = {'type_list':type_list, 'dish_type':self.typ, 'dish_list':show_list}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class details(TemplateView):
    template_name = "details.html"

    def get(self,req):
        ID = req.GET.get('id','')
        if(ID == ''):
            return HttpResponseRedirect('index.html')
        try:
            dish = Dish.objects.get(pk=ID)
        except:
            return HttpResponseRedirect('index.html')
        img_list = Img.objects.filter(dish = dish)
        content={'dish' : dish,'img_list' : img_list}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class chef(TemplateView):
    template_name = "chef.html"

    def get(self,req):
        order_list = Order.objects.filter(paied = 0).order_by('pub_date')
        dish_dict={}
        for item in order_list:
            if(item.dish.name not in dish_dict):
                dish_dict[item.dish.name]=[]
            for i in xrange(1,item.dish.count):
                dish_dict[item.dish.name].add(item.desk.num)
        content={'dish_dict':dish_dict}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class clerk(TemplateView):
    template_name = "clerk.html"

    def get(self,req):
        desk_num = req.GET.get('desk_num','')
        if(desk != ''):
            order_list=Order.objects.filter(desk__num=desk_num)
            for i in order_list:
                i.paied = 1
        content = {}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

    def post(self,req):
        desk_num = req.GET.gets('keywords','') 
        order_list = Order.objects.filter(desk__num = desk_num)
        dic = {}
        for i in order_list:
            for j in i.dish.all():
                if (j.name not in dic):
                    dic[j.name]=j
                else:
                    dic[j.name].count+=j.count
        dish_list = []
        s=0
        for i in dic.values():
            dish_list.add(i)
            s+=i.price*i.count
        content = {'dish_list':dish_list,'sum':s,'desk_num':desk_num}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

