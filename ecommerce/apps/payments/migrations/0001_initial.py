# Generated by Django 3.2.5 on 2021-07-18 20:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.order')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payments.payment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
