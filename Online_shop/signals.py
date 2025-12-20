import json
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from uuid import uuid4
from django.dispatch import receiver
from .models import Product
from django.core.mail import send_mail
from django.contrib.auth.models import User
from config.settings import BASE_DIR

@receiver(post_save, sender=Product)
def send_message_after_save(sender,instance,created,**kwargs):
    if created:
        instance.code = str(uuid4())
        instance.save()
        print('*****************')
        print(f'{instance.name} is  successfull created')
        print('****************')
        send_mail(
            f'Product created',
            'Product Suceessfully created',
            'madi.ismail2108@gmail.com',
            [user.email for user in User.objects.all()],
            fail_silently=False
        )

        
@receiver(pre_delete,sender=Product)
def save_product(sender,instance,**kwargs):
    file_path = f'{BASE_DIR}/ecommerce/save_products/product_{instance.id}.json'
   
    product_data = {
        'id':instance.id,
        'name':instance.name,
        'description':instance.description,
        'price':instance.price,
        'discount':instance.discount,
        'amount':instance.amount,
        'code':instance.code
    }
  
    with open(file_path,'+w') as f:
        json.dump(product_data,f,indent=4,default=str)
    
def decrease_product_amount(sender, instance, **kwargs):
    if instance.amount > 0:
        instance.amount -= 1
        instance.save()