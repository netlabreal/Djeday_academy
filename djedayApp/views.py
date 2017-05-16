from django.shortcuts import render, HttpResponse, render_to_response
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.mail import send_mail

from .forms import FormCandidate
import random, json
from django.core import serializers

from .models import Planet, Candidates, Djeday, SpisokVoprosov, Voprosi, Otveti

# Create your views here.


def index(request):
    return render_to_response('index.html', {})


def ajax(request):
    param = 0
    if request.is_ajax and request.method == 'POST':
        if 'par' in request.POST:
            param = request.POST['par']
        # All planets
        if param == '1':
            planet = Planet.objects.all()
            rez = {}
            for k in planet:
                rez[k.id] = k.name
            return JsonResponse(rez)
        # All djedays
        if param == '2':
            djedays = Djeday.objects.all()
            rez = {}
            for k in djedays:
                rez[k.id] = k.name + '   ('+k.planet.name+')'
            return JsonResponse(rez)
        # Random voprosi
        if param == '3':
            voprosi = SpisokVoprosov.objects.all()
            real = [v.id for v in voprosi]
            # Определение случайного списка вопросов
            n = random.randint(0, len(real)-1)
            sp = SpisokVoprosov.objects.get(id=real[n])
            # Возвращаем список вопросов по коду ордена
            spisok = Voprosi.objects.filter(code=sp)
            rez = {}
            for k in spisok:
                rez[k.id] = k.naim
            return JsonResponse(rez)
        # Список кандидатов, сдавших тест
        if param == '4':
            try:
                cand = Candidates.objects.all()
                # Определяем кандидатов, у которых тест пройден.
                real = [v for v in cand if v.spisok(request.POST['djeday'])]
                posts_serialized = serializers.serialize('json', real)
                #print(posts_serialized)
            except Candidates.DoesNotExist:
                posts_serialized = None
            return JsonResponse(posts_serialized, safe=False)
        if param == '5':
            try:
                r_cand = Candidates.objects.get(id=request.POST['cand'])
                r_cand.master = Djeday.objects.get(id=request.POST['djed'])
                # Проверка на количество падаванов у мастера
                if r_cand.master.kol_padavan()<=2:
                # if Candidates.objects.filter(master=Djeday.objects.get(id=request.POST['djed'])).count()<=2:
                    r_cand.save()
                    send_mail('Congratulation candidate.', r_cand.name+', You are padavan now.', 'from@example.com',
                              [r_cand.email], fail_silently=False)

                    rez = {"rez": 1}
                else:
                    rez = {"rez": 2}
            except Exception:
                rez = {"rez": 0}
            return JsonResponse(rez)
        else:
            rez = {"rez": 0}
            return JsonResponse(rez)
    else:
        return HttpResponse("noneG")

# Создание кандидата, проверка формы
def new_candidate(request):
    if request.is_ajax and request.method == 'POST':
        f = FormCandidate(request.POST)
        if f.is_valid():
            cand = Candidates()
            cand.name = f.cleaned_data['name']
            cand.age = f.cleaned_data['age']
            cand.email = f.cleaned_data['email']
            cand.planet = Planet.objects.get(id=f.cleaned_data['planet'])
            cand.save()
            rez = {"rez": cand.id}
        else:
            rez = {"rez": 0}
        return JsonResponse(rez)

# Внести ответ
def ins_otvet(request):
    if request.is_ajax and request.method == 'POST':
        kk = json.loads(request.POST.getlist('result')[0])
        for k in kk:
            otvet = Otveti()
            otvet.vopros = Voprosi.objects.get(id=k['id'])
            otvet.candidate = Candidates.objects.get(id=k['user'])
            otvet.otvet = k['value']
            otvet.save()
        rez = {"rez": 1}
    else:
        rez = {"rez": 0}
    return JsonResponse(rez)


# Отчет1
class DisplayReport(TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super(DisplayReport, self).get_context_data(**kwargs)
        context['report'] = Otveti.objects.filter(candidate__id=self.kwargs.get('u_id', None))
        context['cand'] =  Candidates.objects.get(id=self.kwargs.get('u_id', None))
        return context


# Дополнительный Отчет
class DisplayAllDjed(TemplateView):
    template_name = "report_djed.html"

    def get_context_data(self, **kwargs):
        context = super(DisplayAllDjed, self).get_context_data(**kwargs)
        d = Djeday.objects.all()
        context['kol'] = [[v, v.kol_padavan()] for v in d]
        return context
