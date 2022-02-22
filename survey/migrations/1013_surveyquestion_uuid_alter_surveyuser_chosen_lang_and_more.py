# Generated by Django 4.0.1 on 2022-01-25 19:46

from django.db import migrations, models, connection
import django.db.models.deletion
from django.db.models import Max
from survey.models import (
    SurveyUser,
    SurveyQuestion,
    SurveyUserQuestionSequence,
    SurveyAnswerQuestionMap,
    SURVEY_STATUS_IN_PROGRESS
)


def migrate_to_current_question(apps, schema_editor):
    sql = (
        "update survey_surveyuser as u set current_question_id = ("
        + "select id from survey_surveyquestion as q where qindex = u.current_qindex);"
    )
    with connection.cursor() as c:
        c.execute(sql)


def create_existing_users_sequences(apps, schema_editor):
    if not SurveyAnswerQuestionMap.objects.exists():
        max_qindex = SurveyQuestion.objects.aggregate(Max("qindex"))["qindex__max"]
        questions = SurveyQuestion.objects.filter(qindex__gt=0).order_by("qindex")
        cursor = connection.cursor()
        cursor.execute("SELECT id, current_qindex, status FROM survey_surveyuser")
        for user in cursor.fetchall():
            user_obj = SurveyUser.objects.get(id=user[0])
            for x in range(0, max_qindex):
                has_been_answered = True
                if user[1] < x+1 or (
                    user[2] == SURVEY_STATUS_IN_PROGRESS
                    and user[1] == x+1
                ):
                    has_been_answered = False

                SurveyUserQuestionSequence.objects.create(
                    user=user_obj,
                    question=questions[x],
                    index=x+1,
                    has_been_answered=has_been_answered,
                )


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "1012_surveyquestion_tooltip_surveyquestionanswer_tooltip"),
    ]

    operations = [
        migrations.CreateModel(
            name="SurveyUserQuestionSequence",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("branch", models.SmallIntegerField(default=0)),
                ("level", models.SmallIntegerField(default=1)),
                ("index", models.IntegerField(default=1)),
                ("has_been_answered", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.surveyquestion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.surveyuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "question", "branch")},
            },
        ),
        migrations.CreateModel(
            name="SurveyAnswerQuestionMap",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("branch", models.SmallIntegerField(default=0)),
                ("level", models.SmallIntegerField(default=1)),
                ("order", models.IntegerField()),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.surveyquestionanswer",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.surveyquestion",
                    ),
                ),
            ],
            options={
                "unique_together": {("answer", "question", "branch")},
            },
        ),
        # We need to update the existed records based on current_qindex.
        migrations.AddField(
            model_name="surveyuser",
            name="current_question",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="survey.surveyquestion",
            ),
        ),
        migrations.RunPython(migrate_to_current_question),
        # Recreate all the sequences for existing users.
        migrations.RunPython(create_existing_users_sequences),
        migrations.AlterField(
            model_name="surveyuser",
            name="current_question",
            field=models.ForeignKey(
                blank=False,
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="survey.surveyquestion",
            ),
        ),
        migrations.RemoveField(
            model_name="surveyuser",
            name="current_qindex",
        ),
        migrations.AddField(
            model_name="recommendations",
            name="categories",
            field=models.ManyToManyField(
                blank=True, to="survey.SurveyQuestionServiceCategory"
            ),
        ),
    ]
