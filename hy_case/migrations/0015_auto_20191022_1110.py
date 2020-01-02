# Generated by Django 2.2 on 2019-10-22 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hy_case', '0014_auto_20191021_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoCert',
            fields=[
                ('n_id', models.AutoField(primary_key=True, serialize=False)),
                ('n_name', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': '无证户',
                'verbose_name_plural': '无证户',
                'ordering': ['-n_id'],
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-c_time'], 'verbose_name': '网站用户', 'verbose_name_plural': '网站用户'},
        ),
    ]
