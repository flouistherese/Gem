from django.db import models
from django.db.models.base import ModelBase

class ModelMeta(ModelBase):
	def __getitem__(self, key):
		obj = self.objects.get(code = key)
		return obj