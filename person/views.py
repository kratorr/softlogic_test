from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.http import Http404
from django.conf import settings

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, NotFound
from rest_framework.views import APIView

from PIL import Image

from person.utils import get_string_vector, compare_vector
from person.models import Person
from person.serializers import PersonSerializer , PersonUUIDSeriazlier, PersonSerialiserUpdate

from person.utils import CustomAPIException

from rest_framework.decorators import action


class PersonViewSet(viewsets.ModelViewSet):
    """
    Viewset for Person model
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def list(self, request):
        queryset  = Person.objects.all()
        serializer = PersonUUIDSeriazlier(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data['id'], status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
        except:
            raise CustomAPIException({'message': 'person no found'}, status_code=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        try:
            input_image = request.FILES['image']
            im = Image.open(input_image)
            im.verify()
        except Exception as exc:
            raise CustomAPIException({'message': 'invalid image'}, status_code=status.HTTP_400_BAD_REQUEST)
  
        string_vector = get_string_vector(input_image)
        serializer = PersonSerialiserUpdate(instance, {'vector': string_vector}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='compare/(?P<pk2>{})'.format(settings.UUID_REGEXP))
    def compare(self, request, pk2, pk=None):
        try:
            person1 = Person.objects.get(pk=pk)
            person2 = Person.objects.get(pk=pk2)
        except ValidationError:
            raise CustomAPIException({'message': 'invalid uuid'}, status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            raise CustomAPIException({'message': 'person not found'}, status=status.HTTP_404_NOT_FOUND)
    
        if person1.vector and person2.vector:
            result = compare_vector(person1.vector, person2.vector)
            return Response({"result": result})
        else:
            return Response({'message': 'vector does not exist'}, status=status.HTTP_404_NOT_FOUND)
