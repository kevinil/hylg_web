# Generated by Django 2.2 on 2019-08-21 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hy_case', '0008_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_key', models.CharField(default=0, max_length=32, unique=True)),
                ('cust_zihao', models.CharField(max_length=64)),
                ('cust_faren', models.CharField(max_length=32)),
                ('cust_idnum', models.CharField(max_length=32)),
                ('cust_saleaddr', models.CharField(max_length=128)),
                ('cust_idaddr', models.CharField(max_length=128)),
                ('cust_contman', models.CharField(max_length=32)),
                ('cust_contphone', models.CharField(max_length=32)),
                ('cust_special', models.CharField(max_length=32)),
            ],
        ),
    ]
