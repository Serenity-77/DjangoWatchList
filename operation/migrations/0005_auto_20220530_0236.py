# Generated by Django 3.2.13 on 2022-05-30 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_alter_operation_operation_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationdetail',
            name='operation',
        ),
        migrations.RemoveField(
            model_name='operationdetail',
            name='user',
        ),
        migrations.DeleteModel(
            name='Operation',
        ),
        migrations.DeleteModel(
            name='OperationDetail',
        ),
    ]
