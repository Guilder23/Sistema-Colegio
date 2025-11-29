# Generated migration - Add tipo field to Contenido model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profesorprofile_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('texto', 'Texto'),
                    ('video', 'Video'),
                    ('documento', 'Documento'),
                    ('imagen', 'Imagen'),
                    ('multimedia', 'Multimedia'),
                ],
                default='texto',
                max_length=20,
            ),
        ),
    ]
