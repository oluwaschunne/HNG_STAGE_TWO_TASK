from django.urls import path
from . import views

urlpatterns = [
    path('/auth/register', views.RegisterView.as_view(), name='user_registration'),
    path('/auth/login', views.LoginView.as_view(), name='user_login'),
    path('/api/users/<uuid:userId>', views.UserDetailView.as_view(), name='user_detail'),
    path('/api/organisations', views.OrganisationListView.as_view(), name='organisation_list'),
    path('/api/organisations/<uuid:orgId>', views.OrganisationDetailView.as_view(), name='organisation_detail'),
    path('/api/organisations/<uuid:orgId>/users', views.AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
    path('/api/organisations/create', views.CreateOrganisationView.as_view(), name='create_organisation'),
]