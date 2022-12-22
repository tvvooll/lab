from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task, SubmitTaskForm, Client, Supplier
from django.urls import reverse



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def submit(request):
    tasks_table = Task.objects.all().order_by('amount')
    form = SubmitTaskForm(request.POST)
    invl = request.POST.get("invl")
    data = {'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken'),
            'amount': request.POST.get('amount'),
            'client': request.POST.get('client'),
            'supplier': request.POST.get('supplier'),
            'comment': request.POST.get('comment'),
            }
    if invl is None:
        invl = 1
    if int(invl)>1 and form.is_valid():
        abc = form.cleaned_data["amount"]
        for i in range(int(invl)):
            data["amount"] = str(int(data["amount"])+1)
            form = SubmitTaskForm(data)
            form.save()
        return HttpResponseRedirect(request.path_info)
    
    if form.is_valid() and int(invl)==1:
        form.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        'form' : form,
        'submited_tasks' : tasks_table,
    }
    return render(request, 'polls/submit.html', context)