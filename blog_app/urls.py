from django.urls import path, include
# from . import views
from .views import HomeView, PostDetailView, AddPostView, EditPostView, DeletePostView, FilterAuthorView, LikeView, aboutView

#from .views import AddCategoryView, FilterView, CommentView,  DeleteCommentView

urlpatterns = [
    # path('', views.home, name='home'),

    # class based url
    path('', HomeView.as_view(), name='home'),
    path('p/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('create/', AddPostView.as_view(), name='add_post'),
    path('p/edit/<int:pk>', EditPostView.as_view(), name='edit_post'),
    path('p/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    # path('add_category/', AddCategoryView.as_view(), name='add_category'),

    # path('c/<str:cat>', FilterView, name='filter'),
    path('u/<str:id>', FilterAuthorView, name='filter_by'),

    path('like/int:<pk>', LikeView, name='post_like'),
    # path('p/<int:pk>/comment/', CommentView, name="comment"),
    # path('p/<int:pk>/comment/delete',
    #      DeleteCommentView.as_view(), name="del-comment"),

    path('about/', aboutView, name='about'),

]
