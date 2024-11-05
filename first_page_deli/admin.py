from django.contrib import admin
from django.apps import apps
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered

# Group 1 for Brand and Category
group1_models = ['Brand', 'Category']

# Group 2 for the Pizza models
group2_models = ['Pizza', 'PizzaToppings', 'PizzaSauce', 'PizzaCheese', 'PizzaCrust']

# Group 3 for the rest of the models
group3_models = ['HotCase', 'SandwichEndI', 'SandwichEndII', 'Dips', 'CheeseBoard',
                 'ServiceCaseMeats', 'ServiceCaseSalads', 'PackedMeatI', 
                 'PackedMeatII', 'SaladsEnd', 'PizzaAndSalads', 'SoupsAndMeals',
                 'EntertainmentEnd', 'Pasta',]

class DeliAdminSite(AdminSite):
    site_header = "Otter Co-op Deli Administration"
    site_title = "Harry's Admin Portal"
    index_title = "Welcome to Otter Co-op Admin Portal"

    # def each_context(self, request):
    #     context = super().each_context(request)
    #     context['group1_models'] = group1_models
    #     context['group2_models'] = group2_models
    #     context['group3_models'] = group3_models
    #     return context

coop_deli_admin_site = DeliAdminSite(name='custom_admin_site')

app_config = apps.get_app_config('first_page_deli')

for model in app_config.get_models():
    try:
        coop_deli_admin_site.register(model)  # Registering with custom admin site
    except AlreadyRegistered:
        pass
