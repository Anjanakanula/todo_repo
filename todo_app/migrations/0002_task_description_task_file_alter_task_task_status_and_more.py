# Generated by Django 4.2.1 on 2023-06-19 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="description",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="file",
            field=models.FileField(
                default=None, max_length=150, null=True, upload_to="files/"
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="task_status",
            field=models.CharField(
                choices=[("Done", "Done"), ("Pending", "Pending")], max_length=20
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="user",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
