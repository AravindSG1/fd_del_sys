from django.shortcuts import render, redirect
from accounts.forms import *
from .forms import *
from core.views import homepage
from django.contrib.auth.decorators import login_required #for login to work on all pages
from django.contrib.auth import login

# Create your views here.
#-------------------------------------Registration Form------------------------------------------------------
def delivery_agent_form(request):
    if request.method == 'GET':
        form_obj_user = LoginTableForm()
        form_obj_delivery_agent = DeliveryAgentProfileForm()
        return render(request,'delivery/delivery_agent_form.html', {'user':form_obj_user, 'delivery':form_obj_delivery_agent})
    
    elif request.method == 'POST':
        form_obj_user = LoginTableForm(request.POST)
        form_obj_delivery_agent = DeliveryAgentProfileForm(request.POST, request.FILES) 
        print('before if')       
        if form_obj_user.is_valid() and form_obj_delivery_agent.is_valid():
            print('after if condition')
            #save the logintable
            form_obj_user = form_obj_user.save(commit = False)
            form_obj_user.is_delivery = True   #assigning role
            form_obj_user.set_password(form_obj_user.password)  #hashing password
            form_obj_user.save()

            #save delivery_agent profile 
            form_obj_delivery_agent = form_obj_delivery_agent.save(commit= False)
            form_obj_delivery_agent.agent = form_obj_user   #link to logintable instance
            form_obj_delivery_agent.save()
            login(request, form_obj_user)
        return redirect(delivery_agent_dashboard)
    
    else:        
        return redirect(delivery_agent_form)

#---------------------------------------Dashboard------------------------------------------------------------    
from django.utils.timezone import now
def delivery_agent_dashboard(request):
    today = now().date()
    delivery_assignments = request.user.delivery_assignments.filter(assigned_at__date=today)
    total_assignments = delivery_assignments.count()
    out_of_delivery = delivery_assignments.filter(status = 'picked_up').count()
    cancelled = delivery_assignments.filter(status = 'cancelled').count()
    earning_per_delivery = 50 #Rs.50/order
    earning_today = earning_per_delivery * total_assignments

    return render(request, 'delivery/delivery_agent_dashboard.html', 
                  {'total_deliveries':total_assignments, 'out_of_delivery':out_of_delivery,
                   'cancelled':cancelled, 'earning':earning_today})

#-------------------------------------------My Deliveries------------------------------------------------------------
def delivery_agent_mydeliveries(request):
    if request.method == 'GET':     
        current_assignments = request.user.delivery_assignments.filter(status__in = ['assigned', 'picked_up'])        
        completed_assignments = request.user.delivery_assignments.filter(status__in = ['delivered', 'cancelled'])

        return render(request, 'delivery/delivery_agent_mydeliveries.html', {
            'current_assignments':current_assignments, 'completed_assignments':completed_assignments
        })

    elif request.method == 'POST':
        assignment_id = request.POST['assignment_id']
        new_status = request.POST.get('status')
        is_cancel = request.POST.get('cancel')  # Check if Cancel button was clicked
        current_assignment = DeliveryAssignment.objects.get(id=assignment_id)
        
        if is_cancel == 'true':
            new_status = 'cancelled'

        if new_status in ['picked_up', 'delivered', 'cancelled']:
            current_assignment.status = new_status
            current_assignment.save()
        return redirect(delivery_agent_mydeliveries)

#--------------------------------------------Profile----------------------------------------------------------
@login_required(login_url='login_page')
def delivery_agent_profile(request):
    return render(request, 'delivery/delivery_agent_profile.html')

@login_required(login_url='login_page')
def delivery_agent_edit_profile(request):    
    form_obj_user = LoginTableEditForm(instance=request.user)
    form_obj_delivery = DeliveryAgentProfileForm(instance=request.user.deliveryagentprofile)
    form_obj_password = PasswordChangeForm()
    if request.method == 'GET':
        return render(request, 'delivery/delivery_agent_edit_profile.html', 
                    {'form_user':form_obj_user, 'form_delivery':form_obj_delivery, 'form_password':form_obj_password})
    elif request.method == 'POST':
        form_obj_user = LoginTableEditForm(request.POST, instance=request.user)
        form_obj_delivery = DeliveryAgentProfileForm(request.POST, request.FILES, instance=request.user.deliveryagentprofile)
        
        # Check if both password fields are filled
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        password_fields_filled = new_password and confirm_password

        # If user is trying to change password, bind the password form
        if password_fields_filled:
            form_obj_password = PasswordChangeForm(request.POST)
        else:
            form_obj_password = PasswordChangeForm()  # unbound = won't validate or raise errors

        #saving other two forms
        if form_obj_user.is_valid() and form_obj_delivery.is_valid():
            form_obj_user.save()
            form_obj_delivery.save()

            # Handle password update only if both fields filled and valid
            if password_fields_filled and form_obj_password.is_valid():
                new_password = form_obj_password.cleaned_data['new_password']
                request.user.set_password(new_password)
                request.user.save()    
                return redirect('delivery_agent_profile')  # Redirect to the same profile page after saving

    return render(request, 'delivery/delivery_agent_profile.html', {
        'form_user': form_obj_user,
        'form_delivery': form_obj_delivery,        
    })