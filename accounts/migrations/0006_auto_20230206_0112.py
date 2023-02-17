# Generated by Django 3.2.15 on 2023-02-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20230121_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='eight_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='five_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='four_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='nine_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='one_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='seven_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='six_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='three_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='two_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='zero_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='finalresult',
            name='luckyNumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='luckyNumber',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='colour',
            field=models.CharField(blank=True, choices=[('Red', 'Red'), ('Green', 'Green'), ('Blue', 'Blue')], max_length=5),
        ),
    ]
