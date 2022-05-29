from django.apps import AppConfig
# from django.db.utils import IntegrityError


class OperationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operation'

    # def ready(self):
    #     self._maybe_add_operation()
    #     AppConfig.ready(self)
    #
    # def _maybe_add_operation(self):
    #     from operation.models import Operation
    #     for op_name in [Operation.ADD, Operation.EDIT, Operation.READ, Operation.DELETE]:
    #         try:
    #             operation = Operation(operation_name=op_name)
    #             operation.save()
    #         except IntegrityError:
    #             pass
