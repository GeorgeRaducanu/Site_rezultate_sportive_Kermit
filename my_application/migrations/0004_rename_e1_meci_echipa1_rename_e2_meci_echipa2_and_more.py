# Generated by Django 4.1.4 on 2022-12-29 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_application', '0003_meci'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meci',
            old_name='e1',
            new_name='echipa1',
        ),
        migrations.RenameField(
            model_name='meci',
            old_name='e2',
            new_name='echipa2',
        ),
        migrations.RenameField(
            model_name='meci',
            old_name='g1',
            new_name='goluri1',
        ),
        migrations.RenameField(
            model_name='meci',
            old_name='g2',
            new_name='goluri2',
        ),
    ]
