from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import auth
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView

User = get_user_model()
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.content_subtype="html"
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.backend='django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request,user)

        # return redirect('home')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        request = self.request
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("question_home")
        return super(LoginView, self).form_invalid(form)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    else:
        return HttpResponse('YOU HAVE BEEN LOGGED OUT')
