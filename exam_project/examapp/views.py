from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('student_home')
        else:
            messages.success(request,'invalid credentials')
            return redirect('login')
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email Taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save();
                # print('user created')
                return redirect('login')

        else:
            messages.info(request,'password not matched')
            return redirect('register')
        return redirect('/')


    return render(request,"register.html")

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('admin_home')
        else:
            messages.success(request, 'Invalid admin credentials')
            return redirect('admin_login')
    return render(request, 'admin_login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')


# views.py
from django.shortcuts import render, redirect
from .models import Exam, Answer
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def student_home(request):
    return render(request, 'student_home.html')

def admin_home(request):
    return render(request, 'admin_home.html')
@login_required(login_url='login')  # Add this decorator to protect views that require login
def create_question(request):
    if request.method == 'POST':
        question_text = request.POST['question']
        ans1 = request.POST['ans1']
        ans2 = request.POST['ans2']
        ans3 = request.POST['ans3']
        ans4 = request.POST['ans4']

        exam = Exam(user=request.user, question=question_text, ans1=ans1, ans2=ans2, ans3=ans3, ans4=ans4)
        exam.save()
        messages.success(request, 'Question added successfully!')
        return redirect('create_question')

    return render(request, 'create_question.html')

def admin_question_view(request):
    emps = Exam.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'admin_question_view.html', context)

# @login_required(login_url='login')
# def student_view(request):
#     if request.method == 'POST':
#         answers = {}
#         for key, value in request.POST.items():
#             if key.startswith('selected_answer_'):
#                 question_id = key.replace('selected_answer_', '')
#                 answers[question_id] = value
#
#         # Save the answers to the database or process them as needed
#         # For example, you can create a model to store student answers
#
#         messages.success(request, 'Answers submitted successfully!')
#         return redirect('student_view')
#
#     questions = Exam.objects.all()
#     return render(request, 'student_view.html', {'questions': questions})


# @login_required(login_url='login')
# def show_answers(request):
#     # Retrieve submitted answers from the session
#     submitted_answers = request.session.get('answers', {})
#
#     questions = Exam.objects.all()
#     return render(request, 'show_answer.html',{'questions': questions, 'submitted_answers': submitted_answers})

# @login_required(login_url='login')
# def show_answers(request):
#     # Get the logged-in user's answers
#     student_answers = Exam.objects.filter(user=request.user)
#
#     context = {
#         'student_answers': student_answers
#     }
#
#     return render(request, 'show_answer.html', context)
# 222222222222222222222222222222222222222222222222222222222222222222222222222
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, Answer


@login_required(login_url='login')
def student_view(request):
    if request.method == 'POST':
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('selected_answer_'):
                question_id = key.replace('selected_answer_', '')
                answers[question_id] = value

        try:
            for question_id, selected_answer in answers.items():
                question = Exam.objects.get(id=question_id)

                # Check if the answer for this question by this user already exists
                existing_answer = Answer.objects.filter(user=request.user, question=question).first()

                if existing_answer:
                    # If an answer already exists, update it
                    existing_answer.answer_id = selected_answer
                    existing_answer.save()
                else:
                    # If no answer exists, create a new one
                    new_answer = Answer(user=request.user, question=question, answer_id=selected_answer)
                    new_answer.save()

            messages.success(request, 'Answers submitted successfully!')
        except Exception as e:
            messages.error(request, f'Error saving answers: {str(e)}')

        return redirect('student_view')

    questions = Exam.objects.all()
    return render(request, 'student_view.html', {'questions': questions})

def show_answers(request):
    # Fetch the answers for the current user
    student_answers = Answer.objects.filter(user=request.user)

    context = {
        'student_answers': student_answers
    }

    return render(request, 'show_answer.html', context)

@login_required(login_url='login')
def admin_view_answers(request):
    # Fetch all answers with additional information
    all_answers = Answer.objects.select_related('question', 'user')

    context = {
        'all_answers': all_answers
    }

    return render(request, 'admin_view_answers.html', context)