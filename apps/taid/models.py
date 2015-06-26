from django.db import models
from django.core.exceptions import ValidationError

import constants


class _Person(models.Model):
    utorid = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Instructor(_Person):
    pass


class TeachingAssistant(Instructor):
    pass


class Student(_Person):
    number = models.PositiveIntegerField()
    ids = models.ManyToManyField("Identification", blank=True)


class Identification(models.Model):
    description = models.CharField(max_length=500)
    value = models.CharField(max_length=100)


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=254)
    section = models.CharField(max_length=1, choices=constants._SECTION_CODES)
    session = models.CharField(max_length=2, choices=constants._SESSION_CODES)
    instructors = models.ManyToManyField("Instructor", blank=True)
    students = models.ManyToManyField("Student", blank=True)
    tuts = models.ManyToManyField("Tutorial", blank=True)
    pracs = models.ManyToManyField("Practical", blank=True)

    def __unicode__(self):
        return self.code


class Tutorial(models.Model):
    code = models.CharField(max_length=20)
    ta = models.ForeignKey(Instructor)

    def __unicode__(self):
        return self.code


class Practical(models.Model):
    code = models.CharField(max_length=20)
    ta = models.ForeignKey(Instructor)

    def __unicode__(self):
        return self.code


class Assignment(models.Model):
    name = models.CharField(max_length=254)
    total = models.DecimalField(max_digits=6, decimal_places=3)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="subparts")

    def __unicode__(self):
        return self.name


class Mark(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=3)
    student = models.ForeignKey("Student")
    gradefile = models.ForeignKey("Grade")

    def __unicode__(self):
        return "{0} ({1}): {2}/{3}".format(
                self.gradefile.assignment.name,
                self.student,
                self.value,
                self.gradefile.assignment.total,
                )

    def clean(self):
        if self.value > self.gradefile.assignment.total:
            raise ValidationError("{0} is more than {1}".format(
                self.value,
                self.gradefile.assignment.total,
                ))
        elif self.value < 0.0:
            raise ValidationError("{0} is less than 0.0".format(self.value))


class Grade(models.Model):
    assignment = models.ForeignKey("Assignment")
    marks = models.ManyToManyField("Mark", blank=True)

    def __unicode__(self):
        return "Grades for {0}".format(self.assignment)


class GradeFile(models.Model):
    name = models.CharField(max_length=254)
    definitions = models.ManyToManyField("GradeDefinition", blank=True)


class GradeDefinition(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=6, decimal_places=3)
    assignment = models.ForeignKey("Assignment")
    parent = models.ForeignKey("self", null=True, blank=True, related_name="subdefinitions")
