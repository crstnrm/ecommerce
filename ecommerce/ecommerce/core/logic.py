from abc import ABC
from typing import Any, Dict, List, Optional, Tuple

from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer

from .serializers import get_serializer


class BaseLogic(ABC):
    """Common model logic."""

    def __init__(self):
        self._model = None
        self._serializer = None

    @property
    def model(self) -> Model:
        if self._model is None:
            raise NotImplementedError(
                'Subclasses must be define model classes.'
            )
        return self._model

    @model.setter
    def model(self, value: Model) -> None:
        self._model = value

    @property
    def serializer(self) -> ModelSerializer:
        if self._serializer is None:
            return get_serializer(self.model)
        return self._serializer

    @serializer.setter
    def serializer(self, value):
        self._serializer = value

    def create(
        self, 
        instance: Optional[Model] = None,
        partial: Optional[bool] = False, 
        **kwargs
    ) -> Model:
        """ 
        Create a model in the database

        Parameters
        ----------
        kwargs : dict
        Required attributes of entity

        Returns
        -------
        A instance
        """
        serializer = self.serializer(
            instance, data=kwargs, partial=partial
        )
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return instance

    def update(self, instance: Model, **kwargs) -> Model:
        """ 
        Update a model in the database

        Parameters
        ----------
        kwargs : dict
        Required attributes of entity

        Returns
        -------
        A instance
        """
       
        if instance is None:
            raise ValueError('Object can not be none.')
        return self.__create(instance, partial=True, **kwargs)

    def update_or_create(
        self, filters: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Tuple[bool, Model]:
        """ Create or update a model in the database

        Parameters
        ----------
        default: dict
        kwargs : dict
        Required attributes of entity

        Returns
        -------
        A boolean and instance
        """
        created = False
        instance = None
        if filters:
            instance = self.find(**filters).first()

        if instance is None:
            created = True

        return created, self.__create(instance, partial=True, **kwargs)

    def delete(self, pk: int) -> Tuple[bool, Model]:
        """ 
        Delete a model from the database

        Parameters
        ----------
        pk: int or str
        primary key of model

        Returns
        -------
        A boolean
        """
        deleted = False
        instance = self.find(pk=pk).first()
        if instance:
            instance.delete()
            deleted = True
        return deleted, instance

    def find(self, *qargs, **kwargs) -> 'QuerySet[Model]':
        """ 
        Find a record by some criteria

        Parameters
        ----------
        kwargs: dict
        filters of model

        Returns
        -------
        A instance
        """
        return self.model.objects.filter(*qargs, **kwargs)

    def get(self, *qargs, **kwargs) -> Model:
        """ 
        Get a record by some criteria

        Parameters
        ----------
        kwargs: dict
        filters of model

        Returns
        -------
        A instance
        """
        return self.model.objects.get(*qargs, **kwargs)

    def serialize(
        self, 
        instance: Optional[Model] = None, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        return self.serializer(instance, **kwargs).data
    
    # Private attributes (Name Mangling)
    __create = create
