from django.urls import path
from .views import CandidateCreateView, CandidateUpdateView, CandidateDeleteView, search_candidates

urlpatterns = [
    path('candidates/', CandidateCreateView.as_view(), name='create-candidate'),
    path('candidates/<int:id>/', CandidateUpdateView.as_view(), name='update-candidate'),
    path('candidates/<int:id>/delete/', CandidateDeleteView.as_view(), name='delete-candidate'),
    path('candidates/search/', search_candidates, name='search-candidates'),
]