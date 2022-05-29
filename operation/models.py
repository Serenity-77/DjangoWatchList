from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Operation(models.Model):

    class Meta:
        db_table = "operations"

    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    READ = "read"

    OPERATION_TYPES = [
        (ADD, 'Read'),
        (EDIT, 'Edit'),
        (DELETE, 'Delete'),
        (READ, 'Read')
    ]

    operation_name = models.CharField(
        max_length=6,
        choices=OPERATION_TYPES,
        default=ADD,
        unique=True)



class OperationDetail(models.Model):

    class Meta:
        db_table = "operation_detail"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True)
    operation_date = models.DateTimeField(auto_now=True)
