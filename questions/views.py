from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST



# Create your views here.
def home_screen_view(request):
    print(request.headers)
    return render(request, "base.html", {})

# views.py
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

def question_detail(request, pk):
    question = Question.objects.get(pk=pk)
    answers = question.answer_set.all()
    return render(request, 'questions/question_detail.html', {'question': question, 'answers': answers})
@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()

    return render(request, 'questions/ask_question.html', {'form': form})

@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'questions/answer_question.html', {'form': form, 'question': question})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"User {user.username} registered successfully!")
            return redirect('question_list')
        else:
          print("Signup form is not valid. Errors: ", form.errors)
    else:
        form = UserCreationForm()

    return render(request, 'questions/signup.html', {'form': form})

@login_required
def upvote_answer(request, answer_id):
    # Retrieve the answer object
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # Increment the upvote count
    answer.upvotes += 1
    answer.save()
    
    # Return JSON response with updated vote counts
    return JsonResponse({'upvotes': answer.upvotes, 'downvotes': answer.downvotes})

@login_required
def downvote_answer(request, answer_id):
    # Retrieve the answer object
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # Increment the downvote count
    answer.downvotes += 1
    answer.save()
    
    # Return JSON response with updated vote counts
    return JsonResponse({'upvotes': answer.upvotes, 'downvotes': answer.downvotes})


def logout_view(request):
    # Use the built-in Django logout function
    logout(request)
    # Redirect to a specific page after logout, or use reverse('some_url_name')
    return redirect('question_list')

# Other views for your forum
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"User {user.username} logged in successfully!")  # Print statement for debugging
            return redirect('home')  # Adjust the redirect URL if needed
        else:
            print("Login form is not valid. Errors:", form.errors)  # Print errors for debugging
    else:
        form = AuthenticationForm()
    return render(request, 'questions/login.html')

def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user 
            answer.question = question
             # Assuming you have user authentication
            answer.save()
            print("Answer saved successfully")  

     # Redirect or handle further logic
            return redirect('question_detail', pk=question_id)
    else:
     form = AnswerForm()
    return render(request, 'questions/answer_question.html', {'form': form, 'question': question, 'question_id': question_id})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')  
# Redirect to the login page after logout

def increment_counter(request):
    if request.method == 'POST':
        # Assuming you have a session-based counter
        counter_value = request.session.get('counter', 0)
        counter_value += 1
        request.session['counter'] = counter_value
        return JsonResponse({'counter': counter_value})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def index(request):
    # Retrieve the current counter value from session
    counter_value = request.session.get('counter', 0)
    return render(request, 'index.html', {'counter_value': counter_value})
