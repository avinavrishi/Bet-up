# Generated by Django 3.2.15 on 2023-01-13 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_paymentrecord_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrecord',
            name='paymentSentTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.paymentpartner'),
        ),
    ]
