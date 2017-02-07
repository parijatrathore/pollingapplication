#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
import json

from .models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.all()[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        ctx = super(ResultsView, self).get_context_data()

        polls = self.get_object()

        # for poll in polls:
        #     print poll

        ctx['mydata'] = 'abc'
        return ctx


def compare(item1, item2):
    if item1.votes < item2.votes:
        return -1
    elif item1.votes > item2.votes:
        return 1
    else:
        return 0

class AllResultsView(generic.ListView):
    model = Poll
    template_name = 'polls/allresults.html'
    context_object_name = 'polls'

    def get_context_data(self, **kwargs):
        ctx = super(AllResultsView, self).get_context_data()
        polls = []
        for poll in ctx['polls']:
            polls.append({
                'poll': poll,
                'choices': sorted(poll.choice_set.all(), cmp=compare, reverse=True)
            })

        ctx['polls'] = polls
        # data=[]
        # poll = self.object_list.all()
        # for choice in poll.choice_set.all():
        #     data.append({'x': choice.choice_text, 'y': choice.votes})
        #
        # ctx['my_data'] = json.dumps(data)
        # ctx['poll'] = poll
        return ctx


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choices = request.POST.getlist('choice[]')


    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        for selected_choice in selected_choices:
            choice = p.choice_set.get(pk=selected_choice)
            choice.votes += 1
            choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('all_results'))
