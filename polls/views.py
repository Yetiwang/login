from django.shortcuts import render,redirect
import pyrebase

config = {
  'apiKey': "AIzaSyCby-voeyDPj5CaaH33OJFdRjCMZF45jKs",
  'authDomain': "django-fb531.firebaseapp.com",
  "databaseURL": "https://django.firebaseio.com",
  'projectId': "django-fb531",
  'storageBucket': "django-fb531.firebasestorage.app",
  'messagingSenderId': "5279372713",
  'appId': "1:5279372713:web:2de9975b2423ef0c7b20b8"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def home(request):
    if 'firebase_user_id' in request.session:  # 2. 檢查 session 是否有 'firebase_user_id' (登入邏輯設定的)
        context = {
            'user_email': request.session.get('firebase_email', '用戶'),  # 從 session 獲取 email
            'firebase_user_id': request.session.get('firebase_user_id')   # 從 session 獲取 user_id
        }
        return render(request, 'polls/home.html', context)  # 3. 顯示頁面，同時帶出 user 資料
    else:
        return redirect('/login')  # 1. 改成沒登入，就強制到 /login 頁面er(request, "polls/home.html")

def login(request):
    return render(request, "polls/login.html")

def verify_login(request):
    account = request.POST.get('account', '')
    password = request.POST.get('password', '')
    ischecked = request.POST.get('ischecked', '')
    print('***', account, password, ischecked)
    try:
        user = auth.sign_in_with_email_and_password(account, password)
        print('user', user)
         # 登入成功，將 Firebase 用戶資訊存入 Django session
        request.session['firebase_user_id'] = user['localId']
        request.session['firebase_email'] = user.get('email', account)
        request.session.modified = True
        return redirect("/")
    except:
        print('*** login failed')
        return render(request, "polls/login.html", {'error': 'Login failed. Please check your credentials.'})

def logout(request):
    # 清除與 Firebase 登入相關的 Django session 資訊
    keys_to_delete = ['firebase_user_id', 'firebase_email']
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]

    print("用戶已登出，相關 session 已清除。")
    # 重定向到登入頁面
    return redirect('/login')









