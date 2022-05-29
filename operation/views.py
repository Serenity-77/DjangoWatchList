from django.shortcuts import render
# from .models import OperationDetail, Operation


class OperationMixin:

    operation = "add"

    def save_operation(self, request):
        try:
            op = Operation.objects.get(operation_name=self.operation)
            detail = OperationDetail(operation=op, user=request.user)
            detail.save()
        except:
            pass
