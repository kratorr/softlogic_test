from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

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
        person = get_object_or_404(self.queryset, pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)  
        serializer = PersonSerialiserUpdate(instance, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)

        return Response({'Ok':'ok'})
  


'''
Создать в БД таблицу Person, содержащую следующие поля: 
 - ID (UUID4) 
 - Имя 
 - Фамилия
 - Вектор (сериализованный массив float или Postgres Array, необязательное поле)

Написать REST API сервер со следующим функционалом: 
1) Создание нового объекта Person (POST) с указанием имени и фамилии в теле запроса. Ответ - ID созданного объекта. 
2) Получение ID всех созданных объектов. (GET)
3) Получение информации об объекте по ID (GET). Ответ должен содержать имя, фамилию, наличие или отсутствие вектора.
4) Добавление вектора (PUT multipart/form-data) для объекта по его ID. Вектор нужно получить из фотографии, приведенной к размеру 300х300 пикселей, разложив ее в одномерный массив и осуществив нормализацию (деление каждого элемента на 255).
5) Провести сравнение двух векторов. В запросе указать ID первого и второго объекта, в ответе вернуть евклидово расстояние между векторами
6) Удаление объекта по ID (DELETE).

Тело запроса и ответа во всех пунктах application/json. 
Сервер не должен «падать» при некорректном запросе (например, получение объекта по несуществующему ID)
, в случае некорректных запросов возвращать соответствующий HTTP-код ошибки и сообщение в формате {"message": "something"
'''