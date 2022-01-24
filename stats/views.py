# -*- coding: utf-8 -*-

import sys
from django.conf.global_settings import LANGUAGES
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from csskp.settings import CUSTOM
from survey.lib.utils import tree, mean_list
from survey.models import SurveyUser, SurveyUserAnswer
from survey.reporthelper import calculateResult


def index(request):
    nb_finished_surveys = SurveyUser.objects.filter(status=3).count()
    nb_surveys = SurveyUser.objects.count()
    context = {
        "nb_surveys": nb_surveys,
        "nb_finished_surveys": nb_finished_surveys,
        "python_version": "{}.{}.{}".format(*sys.version_info[:3]),
    }

    return render(request, "survey/stats.html", context=context)


def overall(request):
    """Returns the page which will display some statistics."""
    nb_finished_surveys = SurveyUser.objects.filter(status=3).count()
    nb_surveys = SurveyUser.objects.count()
    last_surveys = SurveyUser.objects.filter(status=3).order_by("-created_at")[:10]
    survey_results = {user.id: calculateResult(user)[0] for user in last_surveys}
    result = {
        "nb_surveys": nb_surveys,
        "nb_finished_surveys": nb_finished_surveys,
        "survey_results": survey_results,
    }

    return JsonResponse(result)


def survey_status_count(request):
    """Returns the count for the SurveyUser status property."""
    result = SurveyUser.objects.values("status").annotate(count=Count("status"))
    status = {1: "In progress", 2: "Under reviews", 3: "Finished"}
    return JsonResponse(
        {status[item["status"]]: item["count"] for item in result.all()}
    )


def survey_language_count(request):
    """Returns the count for the SurveyUser chosen_lang property."""
    result = SurveyUser.objects.values("chosen_lang").annotate(
        count=Count("chosen_lang")
    )
    return JsonResponse(
        {
            [lang for lang in LANGUAGES if lang[0] == item["chosen_lang"]][0][1]: item[
                "count"
            ]
            for item in result.all()
        }
    )


def answers_per_section(request):
    """Return a dict with the mean of the user's answers per section."""
    chart_exclude_sections = ["__context"]
    if "chart_exclude_sections" in CUSTOM.keys():
        chart_exclude_sections = (
            chart_exclude_sections + CUSTOM["chart_exclude_sections"]
        )

    user_evaluations_per_section = tree()
    user_answers = SurveyUserAnswer.objects.order_by(
        "answer__question__qindex", "answer__aindex"
    )
    for user_answer in user_answers:
        if user_answer.uvalue == "1":
            section = user_answer.answer.question.section

            # Validate if the section score should not be presented in the chart.
            if section.label in chart_exclude_sections:
                continue

            if user_answer.user.id not in user_evaluations_per_section[section.label]:
                user_evaluations_per_section[section.label][user_answer.user.id] = 0
            user_evaluations_per_section[section.label][
                user_answer.user.id
            ] += user_answer.answer.score

    result = tree()
    for section_label in user_evaluations_per_section:
        result[section_label] = mean_list(
            user_evaluations_per_section[section_label].values()
        )

    return JsonResponse(result)
