from venv import create
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.

# pybo 목록 출력
def index(request):

    # 입력 파라미터
    page = request.GET.get('page', '1')     # 페이지, 만약 page값 없이 호출된 경우 디폴트로 1 설정

    # 조회
    question_list = Question.objects.order_by('-create_date')       # 질문 목록 데이터, - 기호는 역방향(최신순), 없으면 순방향
    
    # 페이징 처리
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)     # 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지 데이터만 조회하도록 쿼리 변경

    context = {'question_list': page_obj}       # question_list는 페이징 객체(page_obj)
    return render(request, 'pybo/question_list.html', context)      # 파이썬 데이터를 템플릿에 적용하여 HTML로 변환하는 함수 render

# pybo 내용 출력
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

# pybo 답변 등록
@login_required(login_url = 'common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user        # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return redirect('pybo:detail', question_id=question_id)     # 상세화면을 다시 보여주기 위해 redirect 함수 사용

# pybo 질문 등록
@login_required(login_url= 'common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)   # request.POST 에는 화면에서 사용자가 입력한 내용들이 담겨있다.
        if form.is_valid():
            question = form.save(commit=False)  # 임시저장
            question.author = request.user      # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    
    else:
        form = QuestionForm()
    context = {'form': form}    # {'form': form}은 템플릿에서 질문 등록 시 사용할 폼 엘리먼트를 생성할 때 사용
    return render(request, 'pybo/question_form.html', context)   
