from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from rest_framework import status

from game.stone_square_view import square

from game.models import Stone, Field
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from snippets.serializers import SnippetSerializer
from snippets.models import Snippet


def homepage(request):
    return TemplateResponse(request, 'home.html')


class StoneView(DetailView):
    model = Stone
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(StoneView, self).get_context_data(**kwargs)
        context['sq_stone'] = square(self.object.hex)
        return context


class FieldView(DetailView):
    model = Field
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(FieldView, self).get_context_data(**kwargs)
        context['sq_stone'] = square(self.object)
        return context


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
