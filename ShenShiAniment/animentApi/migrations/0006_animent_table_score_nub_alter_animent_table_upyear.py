# Generated by Django 4.0.5 on 2023-07-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animentApi', '0005_rename_urse_leave_word_ursename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animent_table',
            name='score_nub',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='animent_table',
            name='upyear',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
