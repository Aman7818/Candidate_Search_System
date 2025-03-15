from rest_framework import generics, status
from .models import Candidate
from .serializers import CandidateSerializer
from django.db.models import Count, Q, Case, When, IntegerField
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

class CandidateCreateView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class CandidateUpdateView(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Candidate.DoesNotExist:
            raise NotFound({"error": "Candidate not found"})

class CandidateDeleteView(generics.DestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return Response({"message": "Candidate deleted successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_candidates(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"error": "Search query cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    search_terms = query.lower().split()

    # Build query filter for partial matches
    query_filter = Q()
    for term in search_terms:
        query_filter |= Q(name__icontains=term)

    candidates = Candidate.objects.filter(query_filter)

    # Annotate with a relevancy score based on how many terms match
    candidates = candidates.annotate(
        relevancy=Count(
            Case(
                *[When(name__icontains=term, then=1) for term in search_terms],
                output_field=IntegerField(),
            )
        )
    ).order_by('-relevancy')

    if not candidates.exists():
        return Response({"message": "No matching candidates found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
