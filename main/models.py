from django.db import models
from django.utils.timezone import now


class User(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    address = models.TextField(
        default='Not Added'
    )

    city = models.CharField(
        max_length=100,
        default='Unknown'
    )

    state = models.CharField(
        max_length=100,
        default='Unknown'
    )

    pincode = models.CharField(
        max_length=10,
        default='000000'
    )

    def __str__(self):

        return self.name



class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField( max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='Unknown')
    pincode = models.CharField(max_length=10, default='000000')

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    
class Waste(models.Model):
    seller_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='Unknown')
    pincode = models.CharField(max_length=10, default='000000')
    material = models.CharField(max_length=100)
    quantity = models.IntegerField()
    original_quantity = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='waste_images/')
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(
    max_length=50,
    default='Active'
)


    def __str__(self):
        return self.material
    
    
class BuyRequest(models.Model):

    buyer_name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    address = models.TextField()

    waste = models.ForeignKey(Waste, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    
    payment_method = models.CharField(
    max_length=50,
    default='Cash on Delivery'
    )

    status = models.CharField(
    max_length=50,
    default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.buyer_name
    

@property
def sold_quantity(self):

    return self.original_quantity - self.quantity


class WastePrice(models.Model):

    material = models.CharField(max_length=100)

    price = models.IntegerField()

    def __str__(self):

        return self.material



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    user_id = models.IntegerField(default=0)
    buyer_id = models.IntegerField(default=0)
    admin_reply = models.TextField(default='No Reply Yet')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notification(models.Model):

    user_id = models.IntegerField(default=0)

    buyer_id = models.IntegerField(default=0)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.message



class AdminNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message

