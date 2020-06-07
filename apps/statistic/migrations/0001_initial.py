# Generated by Django 2.2.12 on 2020-06-05 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_int', models.IntegerField(verbose_name='IP的10分进制')),
                ('ip_str', models.CharField(max_length=32)),
                ('province', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('x', models.FloatField(verbose_name='经度')),
                ('y', models.FloatField(verbose_name='维度')),
            ],
            options={
                'db_table': 't_site_statistic',
            },
        ),
    ]