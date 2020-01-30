from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from PIL import Image

from core.utils import get_string_vector, compare_vector
from core.models import Person
from core.serializers import PersonSerializer , PersonUUIDSeriazlier, PersonSerialiserUpdate


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
        instance = self.get_object()
        if not instance:
            return Response({'message':'person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PersonSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        try:
            input_image = request.FILES['image']
            im = Image.open(input_image)
            im.verify()
            im = Image.open(input_image) #reopen after verify
            im = im.resize((300,300))
        except Exception as exc:
            return  Response({'message': 'invalid image'}, status=status.HTTP_400_BAD_REQUEST)

        string_vector = get_string_vector(im)
        serializer = PersonSerialiserUpdate(instance, {'vector': string_vector}, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)


@api_view()
def compare(request):
    try:
        person1 = Person.objects.get(pk=request.GET['person1'])
        person2 = Person.objects.get(pk=request.GET['person2'])
    except MultiValueDictKeyError:
        return Response({'message': 'invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'message': 'invalid uuid'}, status=status.HTTP_400_BAD_REQUEST)
    except Person.DoesNotExist:
        return Response({'message': 'person not found'}, status=status.HTTP_404_NOT_FOUND)
   
    if person1.vector and person2.vector:
        result = compare_vector(person1.vector, person2.vector)
        return Response({"result": result})
    else:
         return Response({'message': 'vector is not exist'}, status=status.HTTP_404_NOT_FOUND)
