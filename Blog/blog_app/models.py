from django.db import models
from django.contrib.auth.models import User


class BlogModel(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


#     #blog_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=1000)
#     content = models.TextField()
#     created_by=models.ForeignKey(User,on_delete=DO_NOTHING)
#    # user = models.ForeignKey(User, blank=True , null=True , on_delete=models.CASCADE)
#     #created_at = models.DateTimeField(auto_now_add=True)
#     #upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
