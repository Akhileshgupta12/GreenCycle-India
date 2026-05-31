from urllib import request

from django.db.models import Count

from django.shortcuts import render, redirect
from .models import User, Waste, Buyer, BuyRequest,WastePrice, Contact, Notification, AdminNotification


# 🏠 HOME

def home(request):
    sugarcane = WastePrice.objects.filter(
        material__icontains='Sugarcane'
    ).first()
    coconut = WastePrice.objects.filter(
        material__icontains='Coconut'
    ).first()
    copper = WastePrice.objects.filter(
        material__icontains='Copper'
    ).first()
    iron = WastePrice.objects.filter(
        material__icontains='Iron'
    ).first()
    aluminium = WastePrice.objects.filter(
        material__icontains='Aluminium'
    ).first()
    tin = WastePrice.objects.filter(
        material__icontains='Tin'
    ).first()
    plastic = WastePrice.objects.filter(
        material__icontains='Plastic'
    ).first()
    paper = WastePrice.objects.filter(
        material__icontains='Paper'
    ).first()
    glass = WastePrice.objects.filter(
        material__icontains='Glass'
    ).first()
    rubber = WastePrice.objects.filter(
        material__icontains='Rubber'
    ).first()
    return render(request, 'home.html', {
        'sugarcane_price': sugarcane.price if sugarcane else 0,
        'coconut_price': coconut.price if coconut else 0,
        'copper_price': copper.price if copper else 0,
        'iron_price': iron.price if iron else 0,
        'aluminium_price': aluminium.price if aluminium else 0,
        'tin_price': tin.price if tin else 0,
        'plastic_price': plastic.price if plastic else 0,
        'paper_price': paper.price if paper else 0,
        'glass_price': glass.price if glass else 0,
        'rubber_price': rubber.price if rubber else 0,
    })



# 📦 MATERIAL DETAIL
def material_detail(request, name):
    return render(request, f'materials/{name}.html')


# 🔐 LOGIN
def login_page(request):

    # अगर user already login है
    if request.session.get('user_id'):
        return redirect('/seller-dashboard/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(
            email=email,
            password=password
        ).first()

        if user:
            # session save
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('/')

        else:
            return render(request, 'login.html', {
    'error': 'Invalid email or password'
            })
    return render(request, 'login.html')


# 📝 REGISTER
def register_page(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')


        # existing email check
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already registered! Please login.'
            })

        # new user save
        User.objects.create(
            name=name,
            email=email,
            password=password,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
        
        AdminNotification.objects.create(
            message=f"New Seller Registered: {name}"

        )

        return redirect('/login/')
    return render(request, 'register.html')


# ♻️ SELL WASTE
def sell_page(request):

    # ❌ अगर seller login नहीं है
    if not request.session.get('user_id'):
        return redirect('/seller-login/')

    # ✅ FORM SUBMIT
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        material = request.POST.get('material')
        waste_price = WastePrice.objects.filter(  material__iexact=material).first()
        if not waste_price: return render(request, 'sell.html', { 'error': '❌ Price not set by admin for this material' })
        quantity = request.POST.get('quantity')
        price = waste_price.price
        image = request.FILES.get('image')

        # database save
        Waste.objects.create(
            seller_id=request.session.get('user_id'),
            name=name,
            location=location,
            city=city,
            state=state,
            pincode=pincode,
            material=material,
            quantity=quantity,
            original_quantity=quantity,
            price=price,
            image=image
        )
        
        AdminNotification.objects.create(

         message=f"New Waste Uploaded: {material}"

    )



        return render(request, 'sell.html', {
            'success': '✅ Data submitted successfully!'
        })
   
    return render(request, 'sell.html', {

    'plastic_price':
        WastePrice.objects.filter(
            material__icontains='Plastic'
        ).first().price,

    'glass_price':
        WastePrice.objects.filter(
            material__icontains='Glass'
        ).first().price,

    'paper_price':
        WastePrice.objects.filter(
            material__icontains='Paper'
        ).first().price,

    'iron_price':
        WastePrice.objects.filter(
            material__icontains='Iron'
        ).first().price,

    'copper_price':
        WastePrice.objects.filter(
            material__icontains='Copper'
        ).first().price,

    'aluminium_price':
        WastePrice.objects.filter(
            material__icontains='Aluminium'
        ).first().price,

    'tin_price':
        WastePrice.objects.filter(
            material__icontains='Tin'
        ).first().price,

    'rubber_price':
        WastePrice.objects.filter(
            material__icontains='Rubber'
        ).first().price,

    'coconut_price':
        WastePrice.objects.filter(
            material__icontains='Coconut'
        ).first().price,

    'sugarcane_price':
        WastePrice.objects.filter(
            material__icontains='Sugarcane'
        ).first().price,
})



# 🚪 LOGOUT
def logout_page(request):
    request.session.flush()
    return redirect('/')



def login_options(request):
    return render(request, 'login_options.html')


def register_options(request):
    return render(request, 'register_options.html')


def buyer_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        # existing buyer check
        if Buyer.objects.filter(email=email).exists():
            return render(request, 'buyer_register.html', {
                'error': 'Buyer already registered'
            })

        # save buyer
        Buyer.objects.create(
            name=name,
            email=email,
            password=password,
            city=city,
            state=state,
            pincode=pincode,
        )
        
        AdminNotification.objects.create(

            message=f"New Buyer Registered: {name}"

            )


        return render(request, 'buyer_register.html', {
            'success': 'Registration successful'
        })
    return render(request, 'buyer_register.html')



def buyer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        buyer = Buyer.objects.filter(
            email=email,
            password=password
        ).first()

        if buyer:
            request.session['buyer_id'] = buyer.id
            request.session['buyer_name'] = buyer.name
            return redirect('/buyer-dashboard/')
        else:
            return render(request, 'buyer_login.html', {
                'error': 'Invalid user id. Register first.'
            })
    return render(request, 'buyer_login.html')



def buyer_dashboard(request):

    # buyer login check
    if not request.session.get('buyer_id'):

        return redirect('/buyer-login/')

    buyer_id = request.session.get('buyer_id')

    buyer = Buyer.objects.get(id=buyer_id)

    search = request.GET.get('search')

    sort = request.GET.get('sort')

    city = request.GET.get('city')

    # default waste
    wastes = Waste.objects.all()

    # material search
    if search:

        wastes = wastes.filter(
            material__icontains=search
        )

    # city filter
    if city:

        wastes = wastes.filter(
            city__icontains=city
        )

    # sorting
    if sort == 'low_price':

        wastes = wastes.order_by('price')

    elif sort == 'high_price':

        wastes = wastes.order_by('-price')

    elif sort == 'latest':

        wastes = wastes.order_by('-id')

    elif sort == 'quantity':

        wastes = wastes.order_by('-quantity')

    return render(request, 'buyer_dashboard.html', {

        'wastes': wastes
    })



def buy_page(request):
 # buyer login check
    if request.session.get('buyer_id'):
        return redirect('/buyer-dashboard/')
    else:
        return redirect('/buyer-login/')
    


def buy_request(request, waste_id):
    print("BUY REQUEST PAGE OPENED") 
    waste = Waste.objects.filter(id=waste_id).first()

    # अगर waste नहीं मिला
    if not waste:
        return redirect('/buyer-dashboard/')

    if request.method == 'POST':
        buyer_name = request.POST.get('buyer_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        payment_method = request.POST.get('payment_method')
    # available stock check
        if int(quantity) > int(waste.quantity):
             return render(request, 'buy_request.html', { 
               'waste': waste,
                'error': '❌ Requested quantity exceeds available stock'
    })    
        # save request
        BuyRequest.objects.create(
            buyer_name=buyer_name,
            mobile=mobile,
            address=address,
            waste=waste,
            quantity=quantity,
            payment_method=payment_method
        )
        AdminNotification.objects.create(
             message=f"New Request Received for {waste.material}" 
        )
     
        # seller notification

        Notification.objects.create(
            user_id=waste.seller_id,
            message=f"New request for {waste.material}"
        )
    # buyer notification
        Notification.objects.create(
         buyer_id=request.session.get('buyer_id'),
             message=f"Request submitted for {waste.material}"
)


        # quantity reduce
        waste.quantity -= int(quantity)
        waste.save()

        return render(request, 'buy_request.html', {
            'waste': waste,
            'success': '✅ Request Submitted Successfully!'
        })

    return render(request, 'buy_request.html', {

        'waste': waste
    })



def seller_dashboard(request):

    # seller login check
    if not request.session.get('user_id'):
        return redirect('/seller-login/')
    # current seller id
    seller_id = request.session.get('user_id')
    # seller uploaded wastes
    wastes = Waste.objects.filter(
        seller_id=seller_id
    )
    return render(request, 'seller_dashboard.html', {
        'wastes': wastes
    })


def buyer_profile(request):

    buyer_name = request.session.get('buyer_name')

    requests = BuyRequest.objects.filter(
        buyer_name=buyer_name
    ).order_by('-created_at')

    return render(request, 'buyer_profile.html', {

        'requests': requests
    })



def seller_requests(request, waste_id):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    waste = Waste.objects.get(id=waste_id)

    requests = BuyRequest.objects.filter(
        waste=waste
    ).order_by('-created_at')

    print("TOTAL REQUESTS =", requests.count())

    return render(request,
        'seller_requests.html',
        {
            'requests': requests,
            'waste': waste
        }
    )



def approve_request(request, request_id):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    buy_request = BuyRequest.objects.get(
        id=request_id
    )

    waste = buy_request.waste

    # quantity reduce
    waste.quantity -= buy_request.quantity

    # negative quantity stop
    if waste.quantity < 0:

        waste.quantity = 0

    waste.save()

    buy_request.status = 'Approved'

    buy_request.save()

    
    Notification.objects.create(

         buyer_id=buy_request.waste.id,

         message=f"Your request for {buy_request.waste.material} has been Approved ✅"

    )
    return redirect(
        f'/seller-requests/{buy_request.waste.id}/'
    )




def reject_request(request, request_id):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    buy_request = BuyRequest.objects.get(
        id=request_id
    )
    waste = buy_request.waste

    waste.quantity += buy_request.quantity

    waste.save()
    buy_request.status = 'Rejected'
    buy_request.save()


    Notification.objects.create(

        buyer_id=buy_request.waste.id,

         message=f"Your request for {buy_request.waste.material} has been Rejected ❌"

    )



    return redirect(
        f'/seller-requests/{buy_request.waste.id}/'
    )


def update_request_status(request, request_id, status):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    buy_request = BuyRequest.objects.get(id=request_id)

    buy_request.status = status

    buy_request.save()

    return redirect(
        f'/seller-requests/{buy_request.waste.id}/'
    )


def seller_notification_count(request):

    seller_count = 0
    buyer_count = 0

    # SELLER COUNT
    if request.session.get('user_id'):

        seller_id = request.session.get('user_id')

        seller_count = BuyRequest.objects.filter(
            waste__seller_id=seller_id,
            status='Pending'
        ).count()

    # BUYER COUNT
    if request.session.get('buyer_id'):

        buyer_name = request.session.get('buyer_name')

        buyer_count = Notification.objects.filter(
            buyer_id=request.session.get('buyer_id'),
            is_read=False
        ).count()

    return {

        'pending_requests_count': seller_count,

        'buyer_notification_count': buyer_count
    }



def seller_profile(request):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    seller_id = request.session.get('user_id')

    seller_name = request.session.get('user_name')

    wastes = Waste.objects.filter(
        seller_id=seller_id
    ).order_by('-id')

    total_waste = wastes.count()

    total_quantity = 0

    approved_requests = BuyRequest.objects.filter(
        waste__seller_id=seller_id,
        status='Approved'
    )

    total_sold = 0

    total_earnings = 0

    for waste in wastes:

        total_quantity += waste.quantity

    for req in approved_requests:

        total_sold += req.quantity

        total_earnings += (
            req.quantity * req.waste.price
        )

    return render(
        request,
        'seller_profile.html',
        {
            'wastes': wastes,
            'seller_name': seller_name,
            'total_waste': total_waste,
            'total_quantity': total_quantity,
            'total_sold': total_sold,
            'total_earnings': total_earnings
        }
    )




def seller_settings(request):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    seller_id = request.session.get('user_id')

    seller = User.objects.get(id=seller_id)

    if request.method == 'POST':

        seller.name = request.POST.get('name')
        seller.email = request.POST.get('email')
        seller.password = request.POST.get('password')
        seller.address = request.POST.get('address')
        seller.city = request.POST.get('city')
        seller.state = request.POST.get('state')
        seller.pincode = request.POST.get('pincode')
        seller.save()

        request.session['user_name'] = seller.name

        return redirect('/seller-profile/')

    return render(request,
        'seller_settings.html',
        {
            'seller': seller
        }
    )


def delete_waste(request, waste_id):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    waste = Waste.objects.filter(
        id=waste_id
    ).first()

    if waste:

        waste.delete()

    return redirect('/seller-profile/')



def edit_waste(request, waste_id):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    waste = Waste.objects.get(id=waste_id)

    if request.method == 'POST':

        waste.location = request.POST.get('location')

        waste.city = request.POST.get('city')

        waste.state = request.POST.get('state')

        waste.pincode = request.POST.get('pincode')

        waste.quantity = request.POST.get('quantity')

        image = request.FILES.get('image')

        if image:

            waste.image = image

        waste.save()

        return redirect('/seller-profile/')

    return render(request,
        'edit_waste.html',
        {
            'waste': waste
        }
    )



def buyer_profile(request):

    if not request.session.get('buyer_id'):

        return redirect('/buyer-login/')

    buyer_name = request.session.get('buyer_name')

    requests = BuyRequest.objects.filter(
        buyer_name=buyer_name
    ).order_by('-id')

    total_requests = requests.count()

    approved_count = requests.filter(
        status='Approved'
    ).count()

    pending_count = requests.filter(
        status='Pending'
    ).count()

    rejected_count = requests.filter(
        status='Rejected'
    ).count()

    return render(request,
        'buyer_profile.html',
        {
            'buyer_name': buyer_name,
            'requests': requests,
            'total_requests': total_requests,
            'approved_count': approved_count,
            'pending_count': pending_count,
            'rejected_count': rejected_count
        }
    )


def cancel_request(request, request_id):

    if not request.session.get('buyer_id'):

        return redirect('/buyer-login/')

    buy_request = BuyRequest.objects.filter(
        id=request_id
    ).first()

    if buy_request:

        # quantity restore
        waste = buy_request.waste

        waste.quantity += buy_request.quantity

        waste.save()

        # request delete
        buy_request.delete()

    return redirect('/buyer-profile/')

def buyer_settings(request):

    if not request.session.get('buyer_id'):

        return redirect('/buyer-login/')

    buyer_id = request.session.get('buyer_id')

    buyer = Buyer.objects.get(id=buyer_id)

    if request.method == 'POST':

        buyer.name = request.POST.get('name')

        buyer.email = request.POST.get('email')

        buyer.password = request.POST.get('password')

        buyer.city = request.POST.get('city')

        buyer.state = request.POST.get('state')

        buyer.pincode = request.POST.get('pincode')

        buyer.save()

        request.session['buyer_name'] = buyer.name

        return redirect('/buyer-profile/')

    return render(request,
        'buyer_settings.html',
        {
            'buyer': buyer
        }
    )



def seller_notifications(request):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    seller_id = request.session.get('user_id')

    requests = BuyRequest.objects.filter(

        waste__seller_id=seller_id,
        status='Pending'

    ).order_by('-id')

    return render(
        request,
        'seller_notifications.html',
        {
            'requests': requests
        }
    )


def buyer_notifications(request):
    if not request.session.get('buyer_id'):
        return redirect('/buyer-login/')
    buyer_id = request.session.get('buyer_id')
    notifications = Notification.objects.filter(
        buyer_id=buyer_id
    ).order_by('-id')
    return render(
        request,
        'buyer_notifications.html',
        {
            'notifications': notifications
        }
    )


def seller_history(request):

    if not request.session.get('user_id'):

        return redirect('/seller-login/')

    seller_id = request.session.get('user_id')

    sold_requests = BuyRequest.objects.filter(
        waste__seller_id=seller_id,
        status='Approved'
    ).order_by('-id')

    return render(request,
        'seller_history.html',
        {
            'sold_requests': sold_requests
        }
    )



def buyer_history(request):

    if not request.session.get('buyer_id'):

        return redirect('/buyer-login/')

    buyer_name = request.session.get('buyer_name')

    history = BuyRequest.objects.filter(
        buyer_name=buyer_name
    ).exclude(
        status='Pending'
    ).order_by('-id')

    return render(request,
        'buyer_history.html',
        {
            'history': history
        }
    )


def admin_dashboard(request):

    total_sellers = User.objects.count()

    total_buyers = Buyer.objects.count()

    total_waste = Waste.objects.count()

    total_requests = BuyRequest.objects.count()

    pending_requests = BuyRequest.objects.filter(
        status='Pending'
    ).count()

    approved_requests = BuyRequest.objects.filter(
        status='Approved'
    ).count()

    total_earnings = 0

    approved = BuyRequest.objects.filter(
        status='Approved'
    )
    for req in approved:

        total_earnings += (
            req.quantity * req.waste.price
        )
   
    notifications = AdminNotification.objects.all().order_by('-id')[:10]



    top_cities = Waste.objects.values(
            'city'
            ).annotate(
                total=Count('id')
    ).order_by('-total')[:5]

    return render(request,
        'admin_dashboard.html',
        {
            'total_sellers': total_sellers,
            'total_buyers': total_buyers,
            'total_waste': total_waste,
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'total_earnings': total_earnings,
            'top_cities': top_cities,
            'notifications': notifications
        }
    )




def all_sellers(request):

    sellers = User.objects.all()

    search = request.GET.get('search', '').strip()

    if search:

        sellers = sellers.filter(
            name__icontains=search
        )

    return render(
        request,
        'all_sellers.html',
        {
            'sellers': sellers
        }
    )





def all_buyers(request):

    buyers = Buyer.objects.all()

    context = {
        'buyers': buyers
    }

    return render(
        request,
        'all_buyers.html',
        context
    )


def all_waste(request):

    wastes = Waste.objects.all().order_by('-id')

    context = {
        'wastes': wastes
    }

    return render(
        request,
        'all_waste.html',
        context
    )

def all_requests(request):

    requests = BuyRequest.objects.all().order_by('-id')

    context = {
        'requests': requests
    }

    return render(
        request,
        'all_requests.html',
        context
    )


def pending_requests(request):

    requests = BuyRequest.objects.filter(
        status='Pending'
    ).order_by('-id')

    context = {
        'requests': requests
    }

    return render(
        request,
        'pending_requests.html',
        context
    )


def approved_requests(request):

    requests = BuyRequest.objects.filter(
        status='Approved'
    ).order_by('-created_at')

    return render(
        request,
        'approved_requests.html',
        {
            'requests': requests
        }
    )


def contact(request):

    success = False

    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        message = request.POST.get('message')

        user_id = request.session.get('user_id', 0)

        buyer_id = request.session.get('buyer_id', 0)

        Contact.objects.create(

            name=name,

            email=email,

            message=message,

            user_id=user_id,

            buyer_id=buyer_id

        )

        success = True

    return render(

        request,

        'contact.html',

        {
            'success': success
        }

    )


def contact_messages(request):

    messages = Contact.objects.all().order_by('-id')

    return render(

        request,

        'contact_messages.html',

        {
            'messages': messages
        }

    )

def my_messages(request):

    user_id = request.session.get('user_id', 0)

    buyer_id = request.session.get('buyer_id', 0)

    if user_id:

        messages = Contact.objects.filter(
            user_id=user_id
        ).order_by('-id')

    elif buyer_id:

        messages = Contact.objects.filter(
            buyer_id=buyer_id
        ).order_by('-id')

    else:

        messages = Contact.objects.none()

    return render(

        request,

        'my_messages.html',

        {
            'messages': messages
        }

    )





def delete_message(request, id):

    message = Contact.objects.get(id=id)

    message.delete()

    return redirect('/my-messages/')


def services(request):

    return render(
        request,
        'services.html'
    )


def about(request):

    return render(
        request,
        'about.html'
    )

