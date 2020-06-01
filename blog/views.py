from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_
from django.contrib.auth import logout
from django.db.models import Sum

@login_required(login_url='/register/')
def homepage(request,pk):

    #user=Register.objects.get(pk=pk)
    userr = User.objects.get(username=request.user)
    #print(userr.register.types)

    if str(userr.register.types)=='seller':
        return render(request,'dashboard.html',{'userr':userr})
    else:
        
        return redirect('/error/')
        

    return render(request,'dashboard.html',{{'userr':userr}})


def NoEntry(request):

    return render(request,'NoEntry.html',{})


@login_required(login_url='/register/')
def logoutt(request):
    logout(request)
    return redirect("/register/")

@login_required(login_url='/register/')
def upload(request,pk):
    user = User.objects.get(username=request.user)
    fod=FoodType.objects.all()
    
    
    try:
        if Restaurant.objects.get(owner_id=user.pk):
            s=Restaurant.objects.get(owner_id=user.pk)

            #print(s)
    except Exception as e:
        return redirect("/dash/{}/restaurant_register/".format(user.pk))
    rest=Restaurant.objects.get(owner_id=pk)
    if request.method =='POST':
        us=request.POST['user_']
        img = request.FILES['imgs']
        f_type=request.POST['ftype']
        pric=request.POST['pri']

        get_ftype=FoodType.objects.get(id=f_type)
        #print(get_ftype)

        Food.objects.create(name=us,food_img=img,types=get_ftype,price=pric)

        a = Food.objects.get(name=us)

        #print(get_object_or_404(Food, pk=pk))
        rest=Restaurant.objects.get(owner_id=request.user.id)

        rest.recipe.add(a)
        rest.save()


    #if str(user.types)=='seller':


    return render(request,'upload_recipe.html',{'user':user,'fod':fod,'rest':rest})

@login_required(login_url='/register/')
def restaurant_reg(request,pk):
    try:
        if Restaurant.objects.get(owner_id=request.user.id):
            return HttpResponse("You already registered")
    except Exception as e:
        print('Not register')
    

    if request.method =='POST':
        nam=request.POST['rest_name']
        add=request.POST['address']
        img = request.FILES['imgs']

        user = Register.objects.get(f_name=request.user)

        

        Restaurant.objects.create(owner=user,name=nam,address=add,product_image=img)

        return redirect("/dash/{}/upload/".format(user.pk))


    return render(request,'restaurant_reg.html',{})


def register(request):

    if request.method =='POST':

        us=request.POST['first']
        las=request.POST['last']
        pas=request.POST['pass']
        emai=request.POST['email']
        add=request.POST['city']
        ph=request.POST['ph']


        User.objects.create_user(username=us,email=emai,password=pas,first_name=us,last_name=las)
        a=User.objects.get(username=us)


        Register.objects.create(f_name=a,add=add,phone=ph)

        user = User.objects.get(username=request.user)

        return redirect("/dash/{}/upload/".format(user.pk))
        
    return render(request,'account/login.html',{})



def login(request):
    if request.method =='POST':

        us=request.POST['u']
        pas=request.POST['p']
        user = authenticate(request, username=us,password=pas)
        #print('user.pk')
        if user is not None:
            login_(request, user)
            users=User.objects.get(username=us)
            print(users.pk)

            return redirect("/dash/{}/".format(users.pk))

            #return render(request, 'accounts/login.html',{})
        else:
            return HttpResponse("sorry")


@login_required(login_url='/register/')
def product_list(request,pk):
    try:

        rest=Restaurant.objects.get(owner_id=request.user.id)
    except Exception as e:
        print('Not Restaurant registered')

    s=rest.recipe.all()


    return render(request,'product_list.html',{'rest':rest})

@login_required(login_url='/register/')
def recipe_remove(request, pk):
    post = get_object_or_404(Food, pk=pk)

    post.delete()
    return redirect('/dash/{}/product_list/'.format(request.user.pk))



@login_required(login_url='/register/')
def recipe_edit(request,pk):
    global img

    post = get_object_or_404(Food, pk=pk)
    print(post)

    if request.method== 'POST':
        nam=request.POST['name']
        #img = request.FILES['imgs']
        pric=request.POST['pri']
        #if request.FILES['imgs'] == None:
        #    print('null')

        obj = Food.objects.get(pk=pk)

        try:
            if request.FILES['imgs']:
                img = request.FILES['imgs']
                obj.food_img=img
                print('pass')
        except Exception as e:
            print('hello')



        

        obj.name=nam
        
        obj.price=pric
        obj.save()

        return redirect('/dash/{}/product_list/'.format(request.user.pk))

    return render(request,'recipe_edit.html',{'post':post})



@login_required(login_url='/register/')
def order_page(request,pk):
    rest=Restaurant.objects.get(owner_id=pk)
    try:

        rest=Restaurant.objects.get(owner_id=pk)
    except Exception as e:
        print('Not Restaurant registered')

    bill=Orders.objects.filter(Restaurant_id=rest.pk)
   
    return render(request,'orders.html',{'bill':bill})

@login_required(login_url='/register/')
def status(request,pk):
    
    post = get_object_or_404(Orders,pk=pk)
    if post.status==True:

        post.status=False
        post.save()
    else:
        post.status=True
        post.save()

    return redirect('/dash/{}/orders/'.format(request.user.pk))



@login_required(login_url='/register/')
def create_order(request,pk):
    
    bill=Orders.objects.filter(Restaurant_id=pk)

    try:

        rest=Restaurant.objects.get(owner_id=pk)
    except Exception as e:
        print('Not Restaurant registered')
    
    rst=Register.objects.all()

    if request.method =='POST':

        customer=request.POST['cust']
        fd=request.POST['food']
        user = User.objects.get(pk=customer)
        
        
        Orders.objects.create(Restaurant=rest,From_order=user)
        for i in fd:
            
            add=Orders.objects.latest('Restaurant')
            print(add)
            add.order.add(i)
            add.save()

    return render(request,'orders_create.html',{'bill':bill,'rest':rest,'rst':rst})