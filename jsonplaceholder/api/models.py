from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    # address 
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    # geo 
    lat = models.DecimalField(decimal_places=4, max_digits=8)
    lng = models.DecimalField(decimal_places=4, max_digits=8)

    phone = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    
    # company
    companyname = models.CharField(max_length=100, default="")
    catchPhrase = models.CharField(max_length=100)
    bs = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Todo(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()

    def __str__(self):
        return self.title

class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    albumId = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    thumbnailUrl = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.name
