# Generated by Django 4.2.1 on 2023-05-20 13:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='member',
        ),
        migrations.RemoveField(
            model_name='income',
            name='source',
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('I', 'Income'), ('E', 'Expenditure')], default='', max_length=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Tithe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('ref_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.member')),
            ],
        ),
    ]
