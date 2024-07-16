from django.db import models
from user_management.models import Student, Invigilator

# Create your models here.
class Card(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self):
        return self.description

class RedCard(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(Invigilator, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Increase the student's threshold
        self.student.threshold += self.card.points
        self.student.save()

        # Check if adding this RedCard triggers adding the student to the Blacklist
        if self.student.threshold >= 20:
            self.add_to_blacklist()

    def add_to_blacklist(self):
        # Create or update the Blacklist entry for the student
        blacklist, created = Blacklist.objects.get_or_create(student=self.student)

    def __str__(self):
        return f"RedCard issued to {self.student.user.fullname} for {self.card.description}"

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    invigilators = models.ManyToManyField(Invigilator)

    def __str__(self):
        return self.title

class Blacklist(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100, editable=False) 
    threshold = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.student_name = self.student.user.fullname
        self.threshold = self.student.threshold
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Blacklisted Student: {self.student_name} (Threshold: {self.threshold})"
