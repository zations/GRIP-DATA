from django.db import migrations

def backfill_tags(apps, schema_editor):
    Note = apps.get_model('core', 'Note')
    for n in Note.objects.filter(tag__isnull=True):
        n.tag = "general"
        n.save(update_fields=["tag"])

class Migration(migrations.Migration):

    dependencies = [
    ("core", "0003_alter_note_tag"),
]

    operations = [
        migrations.RunPython(backfill_tags),
    ]
