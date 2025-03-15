from rest_framework import generics
from django.db.models import Q, Count, Case, When, IntegerField
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework import status

class CandidateCreateView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateUpdateView(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'id'


class CandidateDeleteView(generics.DestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Candidate deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_candidates(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response([])

    search_terms = query.lower().split()

    # Build Q objects to filter names containing at least one search term
    query_filter = Q()
    for term in search_terms:
        query_filter |= Q(name__icontains=term)

    # Fetch candidates with partial matches
    candidates = Candidate.objects.filter(query_filter)

    # Annotate relevancy based on the number of matching words
    candidates = candidates.annotate(
        relevancy=Count(
            Case(
                *[When(name__icontains=term, then=1) for term in search_terms],
                output_field=IntegerField(),
            )
        )
    ).order_by('-relevancy')

    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)