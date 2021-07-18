from ecommerce.core.serializers import InputPagedViewSerializer, OutputPagedViewSerializer
from rest_framework import status
from rest_framework.response import Response

from ecommerce.core.logic import BaseLogic
from ecommerce.views import BaseAPIView


class ModelLogicView(BaseAPIView):
    def __init__(self):
        super().__init__()

        self._logic = None

    @property
    def logic(self) -> BaseLogic:
        if self._logic is None:
            raise NotImplementedError('Subclasses must be define logic.')
        return self._logic

    @logic.setter
    def logic(self, value: BaseLogic) -> None:
        self._logic = value


class BaseView(ModelLogicView):
    def get(self, request, *args, **kwargs):
        
        serializer = InputPagedViewSerializer(data=request.GET.dict())
        serializer.is_valid(raise_exception=True)

        offset = serializer.validated_data['offset']
        limit = serializer.validated_data['limit']
        
        instances = self.logic.find().order_by('id')[offset:limit]
        records = self.logic.serialize(instances, many=True)
        records_len = len(records)

        serializer = OutputPagedViewSerializer({
            'records': records,
            'total_records': records_len,
            'offset': offset,
            'limit': min(limit, records_len)
        })
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = self.logic.create(**request.data)
        data = self.logic.serialize(instance)
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.logic.update(**request.data)
        data = self.logic.serialize(instance)
        return Response(data)


class BaseDetailView(ModelLogicView):
    def get(self, request, pk, *args, **kwargs):
        data = self.logic.serialize(self.logic.get(pk=pk))
        return Response(data)

    def delete(self, request, pk, *args, **kwargs):
        deleted, _ = self.logic.delete(pk=pk)
        if not deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
