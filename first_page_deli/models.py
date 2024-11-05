from django.db import models
from django import forms

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class BaseModel(models.Model):
    item_name = models.CharField(max_length=64)
    category = models.ManyToManyField(Category, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plu = models.IntegerField(default = -1)

    def get_class_name(self):
        return self.__class__.__name__
    
class HotCase(BaseModel):

    class Meta:
        verbose_name = "Hot Case Item"  # Custom name for the model
        verbose_name_plural = "Hot Case Items"

    def __str__(self):
        return self.item_name

class SandwichEndI(BaseModel):

    class Meta:
        verbose_name = 'Sandwich End - I'
        verbose_name_plural = 'Sandwich End - I'

    def __str__(self):
        return self.item_name

class SandwichEndII(BaseModel):

    class Meta:
        verbose_name = 'Sandwich End - II'
        verbose_name_plural = 'Sandwich End - II'

    def __str__(self):
        return self.item_name

class ServiceCaseMeats(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='service_case_meats',
                              null = True, blank = True)

    class Meta:
        verbose_name = "Service Case Meat"
        verbose_name_plural = "Service Case Meats"

    def __str__(self):
        return self.item_name

class ServiceCaseSalads(BaseModel):

    def __str__(self):
        return self.item_name

class PackedMeatI(BaseModel):

    def __str__(self):
        return self.item_name

class PackedMeatII(BaseModel):

    def __str__(self):
        return self.item_name

class SaladsEnd(BaseModel):

    def __str__(self):
        return self.item_name

class PizzaAndSalads(BaseModel):

    def __str__(self):
        return self.item_name

class SoupsAndMeals(BaseModel):

    def __str__(self):
        return self.item_name

class EntertainmentEnd(BaseModel):

    def __str__(self):
        return self.item_name
    
    class Meta:
        verbose_name = "Entertainment End"
        verbose_name_plural = "Entertainment End"

class Pasta(BaseModel):

    def __str__(self):
        return self.item_name

class Dips(BaseModel):
    def __str__(self):
        return self.item_name

class CheeseBoard(BaseModel):

    def __str__(self):
        return self.item_name
    
class PizzaMeat(models.Model):
    meat_name = models.CharField(max_length=128)

    def __str__(self):
        return self.meat_name

class PizzaToppings(models.Model):
    topping_name = models.CharField(max_length=128)

    def __str__(self):
        return self.topping_name

crust_choices = [
    ('reg', 'Regular'),
    ('gl_free', 'Gluten Free'),
]

sauce_choices = [
    ('mar', 'Marinara'),
    ('alf', 'Alfredo')
]

size_choices = [
    ('8', '8'),
    ('13', '13')
]

cheese_choices = [
    ('moz', 'Mozzarella'),
    ('ched', 'Cheddar'),
    ('cmoz', 'Cubed Mozzarella')
]

class Pizza(models.Model):
    item_name = models.CharField(max_length=128)
    category = models.ManyToManyField(Category, blank=True)
    crust = models.CharField(max_length=16, choices=crust_choices, default='reg')
    size = models.CharField(choices=size_choices, max_length=4, default=13)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    sauce = models.CharField(max_length=16, choices=sauce_choices, default='mar')
    meat = models.ManyToManyField(PizzaMeat, blank=True)
    cheese = models.CharField(max_length=16, choices=cheese_choices, default='moz')
    toppings = models.ManyToManyField(PizzaToppings, blank=True)

    def __str__(self):
        return self.item_name
    
    def get_class_name(self):
        return self.__class__.__name__

class BYOPizza(models.Model):
    crust = forms.ChoiceField(choices=crust_choices, label = 'Choose Crust', initial='reg')
    size = forms.ChoiceField(choices=size_choices, label = 'Choose Size', initial=13)
    sauce = forms.ChoiceField(choices=sauce_choices, label = 'Choose Sauce', initial='mar')
    meats = forms.ModelMultipleChoiceField(queryset=PizzaMeat.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Select Meats")
    cheese = forms.MultipleChoiceField(choices=cheese_choices, widget=forms.CheckboxSelectMultiple, label="Select Cheese")
    toppings = forms.ModelMultipleChoiceField(queryset=PizzaToppings.objects.all(), widget=forms.CheckboxSelectMultiple, label="Select Toppings")

    def get_class_name(self):
        return self.__class__.__name__

class OnSaleMeats(models.Model):
    on_sale_meats = models.ManyToManyField(ServiceCaseMeats, blank=True)

    def __str__(self):
        return "On Sale Meats"

class OnSaleSalads(models.Model):
    on_sale_salads = models.ManyToManyField(ServiceCaseSalads, blank=True)

    def __str__(self):
        return "On Sale Salads"
    
    #  Online Ordering

class OrderPizza(models.Model):
    # Pizza details
    crust = models.CharField(max_length=16, choices=crust_choices, default='reg')
    size = models.CharField(max_length=4, choices=size_choices, default='13')
    sauce = models.CharField(max_length=16, choices=sauce_choices, default='mar')
    meat = models.ManyToManyField(PizzaMeat, blank=True)
    cheese = models.CharField(max_length=255)  # Store cheese as a comma-separated string
    toppings = models.ManyToManyField(PizzaToppings, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Order details
    quantity_ordered = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.customer_name} - {self.quantity_ordered} pizza(s)"
