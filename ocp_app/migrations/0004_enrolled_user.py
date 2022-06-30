# Generated by Django 4.0.5 on 2022-06-30 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocp_app', '0003_course_table_educator_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='enrolled_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ocp_app.course_table')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ocp_app.user_details')),
            ],
        ),
    ]
