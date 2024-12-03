from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE localizeaccommodation (
                property_id INTEGER NOT NULL REFERENCES properties_accommodation(id) ON DELETE CASCADE,
                language CHAR(2) NOT NULL,
                description TEXT,
                policy JSONB DEFAULT '{}'::jsonb,
                PRIMARY KEY (property_id, language)  -- Composite primary key
            ) PARTITION BY LIST (language);

            -- Create partitions for specific languages
            CREATE TABLE localizeaccommodation_en PARTITION OF localizeaccommodation FOR VALUES IN ('en');
            CREATE TABLE localizeaccommodation_es PARTITION OF localizeaccommodation FOR VALUES IN ('es');
            CREATE TABLE localizeaccommodation_fr PARTITION OF localizeaccommodation FOR VALUES IN ('fr');
            """,
            reverse_sql="""
            DROP TABLE localizeaccommodation_en;
            DROP TABLE localizeaccommodation_es;
            DROP TABLE localizeaccommodation_fr;
            DROP TABLE localizeaccommodation;
            """
        )
    ]
