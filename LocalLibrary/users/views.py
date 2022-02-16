from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
        username = form.cleaned_data.get('username')
        messages.success(
            request, f'Welcome {username},You Account has been created! Now you can login.')
        return redirect('/')

    else:
        form = UserRegisterForm()
    return render(request, 'catalog/user_form.html', {'form': form})
