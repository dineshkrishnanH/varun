from django.shortcuts import render,redirect

from django.views.generic import View

from budget.forms import ExpenseForm,RegistrationForm,SignInForm

from django.contrib import messages

from django.db.models import Q

from budget.models import Expense

from django.db.models import Count

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User

from budget.decorators import signin_required

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from django.db.models import Sum



decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")

class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()
        
        return render(request,"expense_create.html",{"form": form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"Added successfully")

            return redirect("exp-list")
        
        else:
            messages.error(request,"error")

            return render(request,"expense_create.html",{"form":form_instance})


@method_decorator(decs,name="dispatch")

class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        selected_category=request.GET.get("category","all")

        search_text=request.GET.get("search_text")

        if selected_category=="all":
            # qs=Expense.objects.filter(user=request.user)
            qs=Expense.objects.filter(user=request.user)
        else:
            qs=Expense.objects.filter(category=selected_category,user=request.user)

        if search_text:

            # qs=Expense.objects.filter(user=request.user)
            qs=qs.filter(
                Q(title__contains=search_text)
            )

        return render(request,"expense_list.html",{"expense":qs,"selected":selected_category})


@method_decorator(decs,name="dispatch") 

class ExpenseDetailedView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"expense":qs})

@method_decorator(decs,name="dispatch") 

class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        # extract pk from kwargs
        id=kwargs.get("pk")

        exp_obj=Expense.objects.get(id=id)

        # initialize 
        form_instance=ExpenseForm(instance=exp_obj)


        return render(request,"expense_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        # id extraction
        id=kwargs.get("pk")

        # fetch task object with id
        exp_obj=Expense.objects.get(id=id)

        # initialize form instance with request.POST and instance
        form_instance=ExpenseForm(request.POST,instance=exp_obj)

        #check form has no errors
        if form_instance.is_valid():

             #save from instance
            form_instance.save()

            return redirect("exp-list")
        
        else:
            return render(request,"expense_edit.html",{"form":form_instance})


@method_decorator(decs,name="dispatch")

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        # extract id and delete task object with this id
        Expense.objects.get(id=kwargs.get("pk")).delete()

        return redirect("exp-list")


@method_decorator(decs,name="dispatch")  

class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):
        
        qs=Expense.objects.filter(user=request.user)

        total_expense_count=qs.count()
        
        total_expense_amount = qs.aggregate(Sum('amount'))['amount__sum'] or 0

        food_expense = qs.filter(category='food').aggregate(Sum('amount'))['amount__sum'] or 0

        travel_expense = qs.filter(category='travel').aggregate(Sum('amount'))['amount__sum'] or 0

        health_expense = qs.filter(category='health').aggregate(Sum('amount'))['amount__sum'] or 0

        others_expense = qs.filter(category='other').aggregate(Sum('amount'))['amount__sum'] or 0

        context={
            "total_expense_count":total_expense_count,

            "total_expense_amount": total_expense_amount,

            "food_expense": food_expense,

            "travel_expense": travel_expense,

            "health_expense": health_expense,

            "others_expense": others_expense,
        }
        return render(request,"dash_board.html",context)
    
    

class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        #initialise from with resquest.POST

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)               

            return redirect("signin")
        
        else:

            return render(request,self.template_name,{"form":form_instance})


class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        #initialise from with resquest.POST

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")
            pwd=form_instance.cleaned_data.get("password")

            #authenticate user
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("exp-list")

            return render(request,self.template_name,{"form":form_instance})


@method_decorator(decs,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

@method_decorator(decs,name="dispatch")

class AboutPageView(View):

    def get(self,request,*args,**kwargs):

        return render(request, 'about.html')


class DashBoardView(View):
    
    template_name="dash_board.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)
    