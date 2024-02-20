import os
from django import forms
from django.shortcuts import render, redirect, HttpResponse

from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm
from app01.models import City


class CityForm(BootstrapForm):
    bootstrap_exclude = ['img']
    title = forms.CharField(label='城市')
    count = forms.CharField(label='人口')
    img = forms.FileField(label='LOGO')


class CityModelForm(BootstrapModelForm):
    bootstrap_exclude = ['img']

    class Meta:
        model = City
        fields = "__all__"


def city_list(request):
    queryset = City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


def city_add(request):
    if request.method == "GET":
        form = CityForm()
        return render(request, 'city_add.html', {'form': form})

    form = CityForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        logo_obj = form.cleaned_data.get('img')
        print(type(logo_obj))
        file_path = os.path.join(logo_obj.name)

        f = open(file_path, 'wb')
        for chunk in logo_obj.chunks():
            f.write(chunk)
        f.close()

        context = {
            'title': form.cleaned_data.get('title'),
            'count': form.cleaned_data.get('count'),
            'img': file_path,
        }

        City.objects.create(**context)

        return redirect('/city/list/')
    return render(request, 'city_add.html', {'form': form})


def city_model_add(request):
    if request.method == "GET":
        form = CityModelForm()
        return render(request, 'city_add.html', {'form': form})

    form = CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request, 'city_add.html', {'form': form})
