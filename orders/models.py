
from django.db import models
from Base.models import BaseModel
from accounts.models import ShoppingCart
from django.contrib.auth.models import User

class OrderPlaced(BaseModel):
    order=models.OneToOneField(ShoppingCart,on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    total_amount=models.FloatField()
    Is_order_delivered=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
         if not self.order_number:
            last_order = OrderPlaced.objects.order_by('-created_at').first()

            last_order_number = int(last_order.order_number) if last_order else 20099
            print("Fuck",last_order_number)
            self.order_number = str(last_order_number + 1)
            print(self.order_number)
         super(OrderPlaced, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer.username}"
    def CalcuatePayments(obj):
        amount_paid=0
        amount_pending=0
        for i in obj:
            if i.Is_order_delivered:
                amount_paid+=i.total_amount
            else:
                amount_pending+=i.total_amount
        return amount_paid,amount_pending

