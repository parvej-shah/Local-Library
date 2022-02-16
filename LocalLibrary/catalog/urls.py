from django.urls import path
from django.contrib.auth import views as auth_views
from catalog import views
from users import views as user_views
urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.index, name='home'),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("author/", views.AuthorListView.as_view(), name="author"),
    path("author/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("register/", user_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("myborrowed/", views.UserBorrowedListView.as_view(), name="user_borrowed"),
    path("librarian/", views.Librarian.as_view(), name="librarian"),
    path("book/<uuid:pk>/renewal/", views.book_renewal_form, name="book_renewal"),

]
