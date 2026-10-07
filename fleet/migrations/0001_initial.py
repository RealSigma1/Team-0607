from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name="ID")),
                ("inventory_code", models.CharField(max_length=32, unique=True)),
                ("name", models.CharField(max_length=120)),
            ],
        ),
    ]
