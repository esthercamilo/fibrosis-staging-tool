from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from api.predict import Predict
from drf_yasg import openapi
from rest_framework.decorators import api_view

from core.settings import BASE_DIR


@swagger_auto_schema(operation_id="Predict group", tags=['Prediction'], methods=['post'],
                     manual_parameters=[openapi.Parameter(name="AGE", in_=openapi.IN_QUERY, description="AGE",
                                                          type=openapi.TYPE_INTEGER),
                                        openapi.Parameter(name="AST", in_=openapi.IN_QUERY, description="AST",
                                                          type=openapi.TYPE_NUMBER),
                                        openapi.Parameter(name="ALT", in_=openapi.IN_QUERY, description="ALT",
                                                          type=openapi.TYPE_NUMBER),
                                        openapi.Parameter(name="PL", in_=openapi.IN_QUERY, description="PL",
                                                          type=openapi.TYPE_NUMBER)])
@api_view(['POST'])
def prediction_view(request):
    """
    Prediction of the Fibrosis severity from Molecular Markers
    """
    try:
        data = {k: float(v[0]) for k, v in dict(request.query_params).items()}
        prediction = Predict(root=BASE_DIR).run(data)
        return JsonResponse(prediction, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": 'Fail to predict. Verify if you filled all data correctly. Details: ' + str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def healthcheck(request):
    """
    Verify connection with api
    """
    return JsonResponse({"response": "healthy"}, status=status.HTTP_200_OK)

