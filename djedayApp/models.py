#-*- coding: utf-8 -*-
from django.db import models


# table planet
class Planet(models.Model):
    id = models.AutoField(primary_key=True) # id
    name = models.CharField(max_length=100) # palnet name

    class Meta:
        ordering = ["name"]
        verbose_name = 'planet'  # название приложения в ед.
        verbose_name_plural = 'planets'  # название мн. числ.

    def __str__(self):
        return '%s' % self.name


# таблица джедай
class Djeday(models.Model):
    id = models.AutoField(primary_key=True) # id
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet)

    class Meta:
        ordering = ["name"]
        verbose_name = 'джедай'  # название приложения в ед.
        verbose_name_plural = 'джедаи'  # название мн. числ.

    def kol_padavan(self):
        return Candidates.objects.filter(master=self).count()

    def __str__(self):
        return '[%s] %s -- %s' % (self.id, self.name, self.planet.name)


# таблица кандидатов
class Candidates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet)
    age = models.IntegerField()
    email = models.EmailField()
    master = models.ForeignKey(Djeday, null=True, blank=True)

    #def save(self):
    #    print(self)

    class Meta:
        ordering = ["name"]
        verbose_name = 'кандидат'  # название приложения в ед.
        verbose_name_plural = 'кандидаты'  # название мн. числ.

    # Определяем, пройден ли тест
    def proiden(self):
        rez = False
        otveti = Otveti.objects.filter(candidate=self)
        if otveti.count()>0: rez = True
        return rez

    # Определяем список кандидатов, прошедщих тест по ид джедаев
    def spisok(self, d_id):
        master = Djeday.objects.get(id=d_id)
        print(master)

        if master:
           pl_id = master.planet_id
           if self.planet.id == pl_id and self.otveti_set.all().exists() and self.master is None:
               return self

    def __str__(self):
        return '[%s] %s (%s) - %s' % (self.id, self.name, self.planet.name, self.age)


# таблица наименование списка вопросов
class SpisokVoprosov(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100)

    class Meta:
        ordering = ["code"]
        verbose_name = 'список вопросов'  # название приложения в ед.
        verbose_name_plural = 'список вопросов'  # название мн. числ.

    def __str__(self):
        return '%s' % self.code


# таблица вопросов
class Voprosi(models.Model):
    id = models.AutoField(primary_key=True)
    naim = models.CharField(max_length=100, blank=True)
    code = models.ForeignKey(SpisokVoprosov, null=True)

    class Meta:
        ordering = ["naim"]
        verbose_name = 'вопрос'  # название приложения в ед.
        verbose_name_plural = 'вопросы'  # название мн. числ.

    def __str__(self):
        return '%s --- %s' % (self.naim, self.code)


# таблица ответов
class Otveti(models.Model):
    vopros = models.ForeignKey(Voprosi)
    candidate = models.ForeignKey(Candidates)
    otvet = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'ответ'  # название приложения в ед.
        verbose_name_plural = 'ответы'  # название мн. числ.

    def __str__(self):
        return '%s --- %s' % (self.vopros.naim, self.otvet)
