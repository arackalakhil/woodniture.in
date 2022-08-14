from carts.models import cart, cart_item, coupon
from carts.views import cart_id, offer_check
from django.core.exceptions import ObjectDoesNotExist


def extras(request,total=0, quantity=0, carts_items=None,new_total=0,cart_itemcount=0):
    if "coupon_code" in request.session:
        coupons = coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0
    try:

        if request.user.is_authenticated:
            carts_items = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")[0:2]
            cart_itemcount = carts_items.count()
           
        
     

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_items = cart_item.objects.filter(cart=carts, is_active=True).order_by("id")[0:2]
            cart_itemcount = carts_items.count()
            
            
        for item in carts_items:
            # new_price=offer_price()
            new=offer_check(item)
            print(new) 
            total += new * item.quantity
            print(total)
            quantity += item.quantity
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
    except ObjectDoesNotExist:
        pass
    
    # values = {"total": total, "quantity": quantity, "carts_item": carts_item,"new_total":new_total,"reduction":reduction}
    context = {
        'a':carts_items,
        "new_total": new_total,
        "quantity": quantity,
        "cart_itemcount":cart_itemcount,
    }
    return dict(context)
