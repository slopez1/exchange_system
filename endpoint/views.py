from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import ABSSharedData
from core.security.validators import validate_access


class GenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABSSharedData
        exclude = ['id', 'synchronized', 'created']


class GetDataView(APIView):

    serializers_by_class = {
        # Add your custom serializers for your data custom data
        # Key: SubClass of ABSSharedData
        # Value: Your Serializer
        ABSSharedData: GenericSerializer,
    }

    def get_serializer(self, model):
        return self.serializers_by_class.get(model, GenericSerializer)

    def get(self, request, data_pk):
        data = get_object_or_404(ABSSharedData, pk=data_pk)
        sub_class = ABSSharedData
        for x in ABSSharedData.__subclasses__():
            instance = getattr(data, x.__name__.lower(), None)
            if instance:
                sub_class = x
                data = instance
                break
        if validate_access(data.identifier, request):
            return Response(self.get_serializer(sub_class)(instance=data).data)
        else:
            raise PermissionDenied("You do not have access to this resource {}".format(data.identifier))

# class ExampleView1(StaticDataView):
#     SHARED_DATA_KEY = "Test"
#
#     def process_get(self, request):
#         data = {
#             "paciente": {
#                 "nombre": "Juan Pérez",
#                 "edad": 55,
#                 "sexo": "masculino",
#                 "fecha_ingreso": "2023-06-01",
#                 "diagnostico": "Cáncer de pulmón",
#                 "estado": "hospitalizado",
#                 "habitacion": "301A"
#             },
#             "historia_clinica": {
#                 "antecedentes_personales": {
#                     "tabaquismo": True,
#                     "alergias": ["penicilina", "frutos secos"],
#                     "cirugias_previas": ["apendicectomía"]
#                 },
#                 "resultados_laboratorio": {
#                     "hemoglobina": 12.5,
#                     "glucosa": 110,
#                     "colesterol": 180
#                 },
#                 "tratamiento_actual": {
#                     "medicamentos": ["cisplatino", "docetaxel"],
#                     "dosis": {
#                         "cisplatino": "50 mg/m²",
#                         "docetaxel": "75 mg/m²"
#                     },
#                     "fechas_administracion": {
#                         "cisplatino": ["2023-06-05", "2023-06-12"],
#                         "docetaxel": ["2023-06-08", "2023-06-15"]
#                     }
#                 },
#                 "radioterapia": {
#                     "fechas_sesiones": ["2023-06-10", "2023-06-13", "2023-06-16"],
#                     "dosis_total": "60 Gy"
#                 },
#                 "cirugia": {
#                     "tipo": "lobectomía",
#                     "fecha": "2023-07-02"
#                 }
#             },
#             "notas_enfermeria": [
#                 {
#                     "fecha": "2023-06-01",
#                     "nota": "Paciente ingresado. Estable, sin quejas."
#                 },
#                 {
#                     "fecha": "2023-06-03",
#                     "nota": "Náuseas leves. Administrado antiemético."
#                 },
#                 {
#                     "fecha": "2023-06-06",
#                     "nota": "Fiebre leve. Realizado cultivo de sangre."
#                 }
#             ],
#             "notas_medicas": [
#                 {
#                     "fecha": "2023-06-01",
#                     "nota": "Confirmado diagnóstico de cáncer de pulmón. Iniciar tratamiento de quimioterapia."
#                 },
#                 {
#                     "fecha": "2023-06-15",
#                     "nota": "Tumor reducido en un 30% después del tratamiento de quimioterapia."
#                 },
#                 {
#                     "fecha": "2023-07-02",
#                     "nota": "Cirugía exitosa. Recuperación adecuada."
#                 }
#             ]
#         }
#
#         return Response(data)
#
#
# class ExampleView3(APIView):
#
#     def get(self, request):
#         return Response(request_blockchain_data("Example2"))
#
#
# class ExampleView2(StaticDataView):
#     SHARED_DATA_KEY = "Example2"
#
#     def process_get(self, request):
#         data = {
#             "name": "John Doe",
#             "age": 30,
#             "email": "johndoe@example.com",
#             "is_active": True,
#             "address": {
#                 "street": "123 Main St",
#                 "city": "San Francisco",
#                 "state": "California",
#                 "postal_code": "12345"
#             },
#             "phone_numbers": [
#                 "+1234567890",
#                 "+0987654321"
#             ],
#             "friends": [
#                 {
#                     "name": "Jane Smith",
#                     "age": 28
#                 },
#                 {
#                     "name": "Bob Johnson",
#                     "age": 32
#                 }
#             ],
#             "scores": {
#                 "math": 95,
#                 "english": 87,
#                 "science": 92
#             },
#             "preferences": {
#                 "language": "English",
#                 "theme": "Dark"
#             },
#             "tags": [
#                 "tag1",
#                 "tag2",
#                 "tag3"
#             ],
#             "timestamp": "2023-06-27T12:34:56Z",
#             "is_admin": False,
#             "salary": 5000.50,
#             "skills": [
#                 "Python",
#                 "JavaScript",
#                 "HTML",
#                 "CSS"
#             ],
#             "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
#             "is_verified": True,
#             "birth_date": "1990-01-01",
#             "weight": None,
#             "permissions": {
#                 "read": True,
#                 "write": True,
#                 "execute": False
#             },
#             "avatar_url": "https://example.com/avatar.png",
#             "ratings": [
#                 4.5,
#                 3.8,
#                 5.0
#             ],
#             "has_hobbies": True,
#             "hobbies": [
#                 "Reading",
#                 "Gardening",
#                 "Playing guitar"
#             ],
#             "is_premium": False,
#             "membership_level": "Basic",
#             "last_login": "2023-06-26T18:30:00Z",
#             "is_featured": True,
#             "weight_kg": 75.5,
#             "favorite_colors": [
#                 "Blue",
#                 "Green",
#                 "Red"
#             ]
#         }
#         return Response(data)
