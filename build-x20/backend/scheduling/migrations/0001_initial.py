from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="SchedulingRun", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("algorithm", models.CharField(max_length=40)), ("time_quantum", models.PositiveIntegerField(blank=True, null=True)),
        ("inputs", models.JSONField()), ("results", models.JSONField()), ("created_at", models.DateTimeField(auto_now_add=True)),
    ], options={"ordering": ["-created_at"]})]
