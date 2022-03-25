from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm


# Create your views here.
# 계정생성
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')    # cleaned_data.get 함수는 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password) # 신규 사용자 생성 후 자동 로그인
        # 사용자 인증  
            login(request, user)    # 로그인
            return redirect('index')

    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})