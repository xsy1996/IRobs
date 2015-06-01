from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def get_type_list():
    type_tuple = Dish.objects.values_list('typ').distinct()
    type_list = reduce(lambda x,y:x + y, map(list,type_tuple))
    return type_list

def chef_check(user):
    try:
        if(user.myuser.perm == 3):
            return ture;
    except:
        pass
    return false; 

def clerk_check(user):
    try:
        if(user.myuser.perm == 2):
            return ture;
    except:
        pass
    return false; 

def manager(user):
    try:
        if(user.myuser.perm == 1):
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

    response=['','/','/clerk/','/chef/']

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
        typ = 'recommend'
        dish_list = Dish.objects.filter(typ = typ)
        page_num = req.GET.get('page_num','')
        if(page_num == ''):
            page_num = 1
        type_list = get_type_list()
        paginator = Paginator(dish_list,12) 
        try:
            show_list = paginator.page(page_num)
        except (PageNotAnInteger or EmptyPage):
            show_list = paginator.page(1)
        content = {'type_list':type_list, 'dish_type':typ, 'dish_list':show_list}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

    def post(self,req):
        if(req.POST.get('form_name','') == 'search_form'):
            keywords = req.POST.get('keywords','')
            dish_list = Dish.objects.filter(name__contains = keywords)
            typ = 'all'
            type_list = get_type_list()
            paginator = Paginator(self.dish_list,12) 
            try:
                show_list = paginator.page(self.page_num)
            except (PageNotAnInteger or EmptyPage):
                show_list = paginator.page(1)
            content = {'type_list':type_list, 'dish_type':self.typ, 'dish_list':show_list}
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        elif (req.POST.get('form_name','') == 'select_form'):
            select_dish = req.POST.get('select_dish','')
            dish_list = split(select_dish,'@')
            neworder = Order(
                    desk = Desk.objects.get(pk = req.get_host())
                )
            for i in dish_list:
                neworder.dish.add(Dish.objects.get(pk = i))
            neworder.save()


        
class details(TemplateView):
    template_name = "details.html"

    def get(self,req):
        ID = req.GET.get('id','')
        if(ID == ''):
            return HttpResponseRedirect('/')
        try:
            dish = Dish.objects.get(pk=ID)
        except:
            return HttpResponseRedirect('/')
        img_list = Img.objects.filter(dish = dish)
        content={'dish' : dish,'img_list' : img_list}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

@user_passes_test(chef_check,LOGIN_URL = '/login/')
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

@user_passes_test(clerk_check,LOGIN_URL = '/login/')
class clerk(TemplateView):
    template_name = "clerk.html"

    def get(self,req):
        desk_num = req.GET.get('desk_num','')
        if(desk_num != ''):
            order_list=Order.objects.filter(desk__pk=desk_num)
            for i in order_list:
                i.paied = 1
                i.save()
        content = {}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

    def post(self,req):
        desk_num = req.POST.get('keywords','') 
        order_list = Order.objects.filter(desk__pk = desk_num)
        class temp(objects):
            def __init__(self,name,num = 1,price):
                self.name = name
                self.price = price
                self.num = num

        dic = {}
        for i in order_list:
            for j in i.dish.all():
                if (j.name not in dic):
                    dic[j.name]=temp(j.name,j.num,j.price)
                else:
                    dic[j.name].num+=j.count
        dish_list = []
        s=0
        for i in dic.values():
            i.count = i.price*i.num
            dish_list.append(i)
            s+=i.count
        content = {'dish_list':dish_list,'sum':s,'desk_num':desk_num}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

@user_passes_test(manager_check,LOGIN_URL = '/login/')
class manager_menu(TemplateView):
    template_name = "manager_menu.html"

    def get(self,req):
        dish_list=Dish.objects.all():
        content = {'dish_list':dish_list}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

    def post(self,req):
        operation = req.POST.get('operation','')
        ID = req.POST.get('dish_id','')
        name = req.POST.get('name','')
        price = req.POST.get('price','')
        typ = req.POST.get('type','')
        intro = req.POST.get('intro','')
        if(ID!='')
            dish == dish.objects.get(pk=ID)
        try:
            if(operation == 'remove'):
                dish.delete()
                status = 'success'
            elif(operation == 'edit'):
                dish.name = name
                dish.price = price
                dish.typ = typ
                dish.intro = intro
                dish.save()
                status = 'success'
            elif(operation == 'add'):
                newdish = Dish(
                    name = name,
                    price = price,
                    typ = typ,
                    intro = intro
                    )
                newdish.save()
                status = 'success'
            else:
                status = 'error'
        except:
            status = 'error'
        content = {'status':status}
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
