from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User as DjangoUserModel
from django.db.utils import IntegrityError


from .forms import RegisterForm
from utils.utils import error_message_from_form


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if not form.is_valid():
            content = error_message_from_form(form)
            return HttpResponse(content.strip(), content_type="text/plain", status=422)
        else:
            cleaned_data = form.cleaned_data

            d = {
                'first_name': cleaned_data['firstname'],
                'last_name': cleaned_data['lastname'],
                'username': cleaned_data['username'],
                'password': cleaned_data['password']
            }

            try:
                DjangoUserModel.objects.create_user(**d)
            except IntegrityError as e:
                if hasattr(e, "args") and e.args[0] == 1062:
                    return HttpResponse("Username %s already taken" % (d['username']), content_type="text/plain", status=409)
                raise

            return HttpResponse("", status=200)
    else:
        form = RegisterForm()
        return render(request, "register.html", {'form': form})
