from django.db import models

# Create your models here.
class MainKW(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class GPaaResult(models.Model):
    main_kw = models.ForeignKey(MainKW, on_delete=models.CASCADE)
    parent_kw = models.CharField(max_length=255)
    link = models.TextField()
    title = models.CharField(max_length=255, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.TextField(null=True, blank=True)