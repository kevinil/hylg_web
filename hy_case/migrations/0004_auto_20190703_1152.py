# Generated by Django 2.2 on 2019-07-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hy_case', '0003_casedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casedata',
            name='case_person',
            field=models.CharField(max_length=32),
        ),
    ]
