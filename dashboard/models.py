from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Trainer(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # clients=models.ManyToManyField(Client,blank=True)
    speciality=models.ManyToManyField(Subject)
    image=models.ImageField(upload_to="images",blank=True)
    number=models.CharField(max_length=15, blank=True, null=True, verbose_name='GSM Number')
    # def get_interest_names(self):
    #     return [subject.name for subject in self.speciality.all()]

   
            
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {[subject.name for subject in self.speciality.all()]}"


class Movement(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    sets=models.DecimalField(max_digits=3,decimal_places=0)
    repetition=models.DecimalField(max_digits=3,decimal_places=0)
    calory=models.DecimalField(max_digits=10,decimal_places=3,blank=True)
    videoUrl=models.CharField(max_length=300,blank=True)
    def __str__(self):
        return self.name

class Exercise(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    # sets=models.DecimalField(max_digits=3,decimal_places=0)
    purpose=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True,blank=True)
    sunday=models.ManyToManyField(Movement,blank=True,related_name='sunday_exercises')
    monday=models.ManyToManyField(Movement,blank=True,related_name='monday_exercises')
    tuesday=models.ManyToManyField(Movement,blank=True,related_name='tuesday_exercises')
    wednesday=models.ManyToManyField(Movement,blank=True,related_name='wednesday_exercises')
    thursday=models.ManyToManyField(Movement,blank=True,related_name='thursday_exercises')
    friday=models.ManyToManyField(Movement,blank=True,related_name='friday_exercises')
    saturday=models.ManyToManyField(Movement,blank=True,related_name='saturday_exercises')
    start_date=models.DateField()
    end_date=models.DateField()
    # video=models.URLField()
    def __str__(self):
        return self.name
    
class Food(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    calory=models.DecimalField(max_digits=10,decimal_places=3,blank=True)
    def __str__(self):
        return self.name

class Nutrition(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    sunday=models.ManyToManyField(Food,blank=True,related_name='sunday_nutrition')
    monday=models.ManyToManyField(Food,blank=True,related_name='monday_nutrition')
    tuesday=models.ManyToManyField(Food,blank=True,related_name='tuesday_nutrition')
    wednesday=models.ManyToManyField(Food,blank=True,related_name='wednesday_nutrition')
    thursday=models.ManyToManyField(Food,blank=True,related_name='thursday_nutrition')
    friday=models.ManyToManyField(Food,blank=True,related_name='friday_nutrition')
    saturday=models.ManyToManyField(Food,blank=True,related_name='saturday_nutrition')
    def __str__(self):
        return self.name



class Measurement(models.Model):
    id=models.AutoField(primary_key=True)
    height=models.DecimalField(max_digits=10,decimal_places=3)
    weight=models.DecimalField(max_digits=10,decimal_places=3)
    rate=models.DecimalField(max_digits=10,decimal_places=3)
    # alınan kalori girilecek
    # yakılan kalori
    muscule=models.DecimalField(max_digits=10,decimal_places=3)
    bodyindex=models.DecimalField(max_digits=10,decimal_places=3)
    datenow=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.datenow}"
    


class Client(models.Model):
    id=models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    birthday=models.DateField()
    gender=models.CharField(max_length=100)
    
    number=models.CharField(max_length=15, blank=True, null=True, verbose_name='GSM Number')
    # profilePhoto=models.ImageField()
    image=models.ImageField(upload_to="images",blank=True)
    trainer=models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True,blank=True)
    exerciseProgram=models.ForeignKey(Exercise,on_delete=models.CASCADE,blank=True,null=True)
    nutritionProgram=models.ForeignKey(Nutrition,on_delete=models.CASCADE,blank=True,null=True)
    # measurement=models.ForeignKey(Measurement,on_delete=models.SET_NULL,null=True,blank=True)
    measurement=models.ManyToManyField(Measurement,blank=True)
    purpose=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def save(self, *args, **kwargs):
        if self.purpose and not self.trainer:
            convenient_trainer = Trainer.objects.filter(
                speciality__in=[self.purpose],
            ).annotate(
                ogrenci_sayisi=models.Count('client')
            ).filter(ogrenci_sayisi__lt=5).first()

            if convenient_trainer:
                self.trainer = convenient_trainer

        super().save(*args, **kwargs)



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
# class StudentSubject(models.Model):
#     student=models.ForeignKey(Student, on_delete=models.CASCADE)
#     subject=models.ForeignKey(Subject,on_delete=models.CASCADE)



    

