from django.urls import path
from . import views

'''path() function defines:
    A URL pattern, which is an empty string: ''
    View function that will be called if the URL pattern is detected
    views.index -> function named index() in the views.py file
    name parameter: unique identifier
'''
urlpatterns = [
    path('',views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/',views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name="author-detail"),
]
