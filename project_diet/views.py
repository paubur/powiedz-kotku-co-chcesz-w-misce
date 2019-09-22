from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView

from .models import Cat, Food, Composition, Content
from project_diet.forms import AddUserForm, LoginForm, AddCatForm, AddFoodForm, AddCompositionForm



class AddUserView(FormView):
    def get(self, request):
        form = AddUserForm()
        context = {"form": form,
                   "submit": " Send "}
        return render(request, "form.html", context)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=name, password=password)
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('add_cat'))
            else:
                return redirect(reverse_lazy('add_user'))
        else:
            context = {"form": form,
                       "submit": "Send"}
            return render(request, 'form.html', context)


class LoginView(FormView):
    def get(self, request):
        form = LoginForm()
        context = {"form": form,
                   "submit": "Send"}
        return render(request, "form.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('cats'))
            else:
                message = '<h3>Wrong username or password</h3>'
                context = {"form": form,
                   "submit": "Send",
                    "message": message}
                return render(request, 'form.html', context)
        else:
            context = {"form": form,
                   "submit": "Send"}
            return render(request, 'form.html', context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))



class CatsListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cats = Cat.objects.filter(user_id=request.user).order_by('name')
            context = {"cats": cats}
            return render(request, "cats.html", context)
        else:
            return redirect(reverse_lazy('login'))


class CatDataView(View):
    def get(self, request, name):
        if request.user.is_authenticated:
            cat = Cat.objects.get(name=name, user_id=request.user)
            return render(request, 'cat_data.html', {'cat': cat})
        else:
            return redirect(reverse_lazy('login'))


class AddCatView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddCatForm(initial={'user': request.user})
            context = {
                "form": form,
                "submit": "Send"
            }
            return render(request, 'add_cat.html', context)
        else:
            return redirect(reverse_lazy('login'))

    def post(self, request):
        form = AddCatForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            birthmark = form.cleaned_data['birthmark']
            medical_condition = form.cleaned_data["medical_condition"]
            diet = form.cleaned_data["diet"]
            diet_description = form.cleaned_data["diet_description"]

            cat = Cat.objects.create(name=name, age=age, birthmark=birthmark,
                                     medical_condition=medical_condition, diet=diet,
                                     diet_description=diet_description, user_id=user_id)
            return redirect(reverse_lazy("cats"))
        else:
            context = {
            "form": form,
            "submit": "submit"
            }
            return render(request, 'add_cat.html', context)




class FoodListView(View):
    def get(self, request, cat_id):
        if request.user.is_authenticated:
            food_list = Food.objects.filter(cat=cat_id)
            cat_name = Cat.objects.get(id=cat_id)
            cat_name=cat_name.name
            context = {"food_list": food_list, "cat_id": cat_id, "cat_name": cat_name}
            return render(request, "food_list.html", context)
        else:
            return redirect(reverse_lazy('login'))


class FoodDataView(View):
    def get(self, request, food_company):
        if request.user.is_authenticated:
            food = Food.objects.filter(name=food_company)
            return render(request, 'food_data.html', {'food': food})
        else:
            return redirect(reverse_lazy('login'))



class AddFoodView(View):
    def get(self, request, cat_id):
        if request.user.is_authenticated:
            initial = {"cat": cat_id}
            form = AddFoodForm(initial=initial)
            context = {
                "form": form,
                "submit": "Send"
            }
            return render(request, 'form.html', context)
        else:
            return redirect(reverse_lazy('login'))

    def post(self, request, cat_id):
        form = AddFoodForm(request.POST)
        if form.is_valid():
            cat = Cat.objects.get(id=cat_id)
            company = form.cleaned_data['company']
            name = form.cleaned_data['name']
            food = Food.objects.create(company=company, name=name)
            food.cat.add(cat)
            return redirect(reverse_lazy("food_list", kwargs={'cat_id':cat_id}))
        else:
            context = {
            "form": form,
            "submit": "Send"
            }
            return render(request, 'form.html', context)


class AddCompositionAndContentView(View):
    def get(self, request, food_id):
        if request.user.is_authenticated:

            initial = {"food": food_id}
            form = AddCompositionForm(initial=initial)
            context = {
                "form": form,
                "submit": "Send"
            }
            return render(request, 'form.html', context)
        else:
            return redirect(reverse_lazy('login'))

    def post(self, request, food_id):
        form = AddCompositionForm(request.POST)
        if form.is_valid():
            composition_name = form.cleaned_data['name']
            content_quantity = form.cleaned_data['quantity']
            composition = Composition.objects.get_or_create(name=composition_name)[0]
            food = Food.objects.get(id=food_id)
            try:
                content = Content.objects.get(food=food, composition=composition)
                content.quantity = content_quantity
            except ObjectDoesNotExist:
                content = Content(quantity=content_quantity, food=food, composition=composition)
            content.save()
            return redirect(reverse_lazy('composition', kwargs={"food_id": food_id}))
        else:
            context = {
            "form": form,
            "submit": "submit"
            }
            return render(request, 'form.html', context)


class CompositionAndContentListView(View):
    def get(self, request, food_id):
        if request.user.is_authenticated:

            food = Food.objects.get(id=food_id)
            compositions = food.composition_set.all()
            compositions_list = []
            for composition in compositions:
                compositions_list.append({'name': composition.name, 'quantity': composition.content_set.filter(food=food).first().quantity})

            context = {"compositions": compositions_list, "food_id": food_id}
            return render(request, "composition_content_list.html", context)
        else:
            return redirect(reverse_lazy('login'))


    # re_path(r'^(?P<food_id>(\d)+)/add_composition$', AddCompositionAndContentView.as_view(), name="add_composition"),
# a chcę
    # re_path(r'^food_list/(?P<cat_id>(\d)+)$', FoodListView.as_view(), name="food_list"),


class CompareCompositionView(View):
    def get(self, request, cat_id):
        if request.user.is_authenticated:

            food_list = Food.objects.filter(cat=cat_id)
            compositions = Composition.objects.filter(food__cat__user=request.user).distinct()
            print(compositions, len(compositions))

            quantity_food_composition = []
            for food in food_list:
                quantity_food_composition.append({'food': food, 'quantity': []})
                for composition in compositions:
                    try:
                        quantity_food_composition[-1]['quantity'].append(Content.objects.get(food=food, composition=composition).quantity)
                    except ObjectDoesNotExist:
                        quantity_food_composition[-1]['quantity'].append(0)

            print(quantity_food_composition)

            context = {
                "compositions": compositions,
                "cat_id": cat_id,
                "food_list": food_list,
                "quantity_food_composition": quantity_food_composition
            }
            return render(request,'c.html', context)
        else:
            return redirect(reverse_lazy('login'))