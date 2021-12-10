# Generated by Django 3.2.9 on 2021-12-01 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "1004_delete_translationkey"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveyquestionanswer",
            name="bonus_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="surveyquestionanswer",
            name="dependant_answers",
            field=models.ManyToManyField(
                blank=True,
                related_name="_survey_surveyquestionanswer_dependant_answers_+",
                to="survey.SurveyQuestionAnswer",
            ),
        ),
        migrations.AlterField(
            model_name="surveyuser",
            name="choosen_lang",
            field=models.CharField(
                choices=[("en", "English"), ("fr", "French"), ("de", "German")],
                default="en",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="translation",
            name="lang",
            field=models.CharField(
                choices=[("en", "English"), ("fr", "French"), ("de", "German")],
                default="en",
                max_length=2,
            ),
        ),
    ]