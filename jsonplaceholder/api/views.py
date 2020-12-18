from django.shortcuts import render
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import requests

from .models import User, Todo, Album, Photo, Post, Comment

class ApiPageView(TemplateView):
    def get(self, request, **kwargs):
        users = User.objects.all()
        return render(request, 'api/index.html', {'title': 'Users List', 'users': users})

class UserPageView(TemplateView):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.filter(id=user_id)[0]
        todos = Todo.objects.filter(userId=user_id)

        posts = list(Post.objects.filter(userId=user_id))

        albums = list(Album.objects.filter(userId=user_id))
        for album in albums:
            album.photos = Photo.objects.filter(albumId=album.id)

        return render(request, 'api/users.html', {
            'title': 'User Page',
            'user': user,
            'todos': todos,
            'posts': posts,
            'albums': albums,
        })


class PostPageView(TemplateView):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']
        post_id = kwargs['post_id']
        post = Post.objects.filter(id=post_id)[0]
        comments = Comment.objects.filter(postId=post_id)

        return render(request, 'api/posts.html', {
            'post': post,
            'comments': comments
        })


# Just a test page
class TestPageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://jsonplaceholder.typicode.com/posts'
        req = requests.get(url)
        r = req.json()

        posts = list(Post.objects.filter(userId=1))
        for post in posts:
            post.comments = Comment.objects.filter(postId=1)

        return render(request, 'test.html', {'foo': posts})

# class to fetch data from API and to save it to the database.
class GetUsersPageView(TemplateView):

    def saveComment(commentData):
        comment = Comment()
        comment.id = commentData['id']
        comment.postId = Post.objects.get(id=commentData['postId'])
        comment.name = commentData['name']
        comment.email = commentData['email']
        comment.body = commentData['body']

        comment.save()

    def savePost(postData):
        post = Post()
        post.id = postData['id']
        post.userId = User.objects.get(id=postData['userId'])
        post.title = postData['title']
        post.body = postData['body']

        post.save()

    def savePhoto(photoData):
        photo = Photo()
        photo.id = photoData['id']
        photo.albumId = Album.objects.get(id=photoData['albumId'])
        photo.title = photoData['title']
        photo.url = photoData['url']
        photo.thumbnailUrl = photoData['thumbnailUrl']

        photo.save()

    def saveAlbum(albumData):
        album = Album()
        album.id = albumData['id']
        album.userId = User.objects.get(id=albumData['userId'])
        album.title = albumData['title']

        album.save()

    def saveTodo(todoData):
        todo = Todo()
        todo.id = todoData['id']
        todo.userId = User.objects.get(id=todoData['userId'])
        todo.title = todoData['title']
        todo.completed = todoData['completed']

        todo.save()


    def saveUser(userData):
        user = User()
        user.id = userData['id']
        user.name = userData['name']
        user.username = userData['username']
        user.email = userData['email']
        user.street = userData['address']['street']
        user.suite = userData['address']['suite']
        user.city = userData['address']['city']
        user.zipcode = userData['address']['zipcode']
        user.lat = userData['address']['geo']['lat']
        user.lng = userData['address']['geo']['lng']
        user.phone = userData['phone']
        user.website = userData['website']
        user.companyname = userData['company']['name']
        user.catchPhrase = userData['company']['catchPhrase']
        user.bs = userData['company']['bs']

        user.save()

    
    def getData(res, func):
        url = 'http://jsonplaceholder.typicode.com/' + res
        req = requests.get(url)
        r = req.json()
        for x in r:
            func(x)


    def get(self, request, **kwargs):
        GetUsersPageView.getData('users', GetUsersPageView.saveUser)
        GetUsersPageView.getData('todos', GetUsersPageView.saveTodo)
        GetUsersPageView.getData('albums', GetUsersPageView.saveAlbum)
        # there are too many pictures so I limit them to 5 pictures per album
        # I use loop here to utilize generic function.
        for x in range(0, Album.objects.latest('id').id + 1):
            # fetch 5 items per given albumId
            GetUsersPageView.getData('photos?albumId=' +str(x)+ '&_start=5&_limit=5', GetUsersPageView.savePhoto)
        GetUsersPageView.getData('posts', GetUsersPageView.savePost)
        GetUsersPageView.getData('comments', GetUsersPageView.saveComment)

        return render(request, 'apitest.html', {'foo': 'data fetched'})
