from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views import View
from Frozery.models import customer,order
from Frozery.middlewares.auth_middleware import auth_middleware
# Create your views here.

def logout(request):
    request.session.clear()
    return redirect('login')

class login(View):
    return_url = None
    def get(self,request):
        login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self,request):
        email = request.POST['email']
        password = request.POST['psw']
        try:
            Customer = customer.objects.get(email = email)
        except:
            Customer = False 
        error_message = None

        if Customer:
            flag = check_password(password, Customer.password)
            if flag:
                request.session['Customer'] = Customer.id
                request.session['fname'] = Customer.first_name
                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    return_url = None
                    return redirect('/')

            else:
                error_message = "Invalid Username or Password!!!"  
                return render(request,'login.html', {'error':error_message})
        else:
            error_message = "Invalid Username or Password!!!"
            return render(request,'login.html', {'error':error_message})

def adminlog(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['adminpsw']
        user = auth.authenticate(username = username, password = password)
        orders = order.objects.all().order_by('-date')
        if (user is not None) and (user.is_superuser):
            auth.login(request, user)
            request.session['admin'] = user.id
            return render(request, 'admin.html', {'orders':orders})
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error1': error_message})
    else:
        orders = order.objects.all().order_by('-date')
        payment_status = request.GET.get('payment')
        order_status = request.GET.get('Order')
        print (payment_status, order_status)
        if payment_status:
            Orders = order.objects.filter(id  = payment_status)
            for Order in Orders:
                Order.payment_status = True
                Order.save()
        if order_status:
            Orders = order.objects.filter(id  = order_status)
            for Order in Orders:
                if Order.payment_status:
                    Order.completed = True
                    Order.save()
        
        return render(request, 'admin.html',{'orders':orders})
        


def register(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phoneno = request.POST['phoneno']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['psw']
        passwordr = request.POST['psw-repeat']

        error_message = None
        data = {'first_name': first_name,
        'last_name': last_name,
        'phoneno': phoneno,
        'email': email,
        'address': address}
        # Validation of Customer credentials  
        if not first_name:
            error_message = "First Name Required"
        elif not last_name:
            error_message = "Last Name Required"
        elif not phoneno:
            error_message = "Contact Number Required"
        elif len(phoneno) < 11 :
            error_message = "Inappropriate Contact Number"
        elif not address:
            error_message = "Address Required"
        elif not email:
            error_message = "Email Required"
        elif customer.objects.filter(email = email).exists():
            error_message = "Email Already Exists"
        elif len(password) < 8:
            error_message = "Password length must be greater than 8"
        elif password != passwordr:
            error_message = "OOPS!!! Passwords do not match!!!"
        

        # Saving Customer
        if not error_message:
            Customer = customer(first_name = first_name, Last_name = last_name, phoneno = phoneno, email = email, addr = address, password = password)
            Customer.password = make_password(Customer.password)
            Customer.save()
            messages.info(request,"User Created Succesfully")
            return render(request, 'login.html',{'email' : email}) 
        # Giving Error and fill data    
        else:
            Data = {
                'error': error_message,
                'data' : data
            }
            return render(request, "register.html", Data)
                
        
    else:
        return render(request, 'register.html')