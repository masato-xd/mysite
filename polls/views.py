from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


# Create your views here.

# def index(request):
#     # return HttpResponse("hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     template = loader.get_template('polls/index.html')
#
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#
#     # return HttpResponse(output)
#     # return HttpResponse(template.render(context, request))
#     # print(request, context)
#
#     # render函数会返回一个经过字典数据渲染过的模板封装而成的HttpResponse对象
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # print(question)
#     # return render(request, 'polls/detail.html', {'question': question})
#
#     question = get_object_or_404(Question, pk=question_id)
#     # print(dir(question))
#     # print(type(question))
#     # 打印类型，可以看出返回的是一个Httpresponse对象
#     # print(type(render(request, 'polls/detail.html', {"question": question})))
#     return render(request, 'polls/detail.html', {"question": question})


# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """返回最近发布的5个问卷."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    # print(type(request.POST))
    # print(type(request.POST['choice']))
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        # 发生choice未找到异常时，重新返回表单页面，并给出提示信息
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice.",
                                                     })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
