from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

from .models import SurveyTitle


# class SurveyTitleViewSets(ModelViewSet):
#     queryset = SurveyTitle.objects.all()
#     serializer_class = SurveyTitleSerializer


@api_view(['GET', 'POST'])
def recommand_category(request):
    if request.method == 'GET':
        data = json.loads(request.body)

        result = keyword_match(data.get('titles'), data.get('categories'))
        return Response(result)

    if request.method == 'POST':
        data = json.loads(request.body)
        surveyTitle = SurveyTitle()
        surveyTitle.title = data.get('title')
        surveyTitle.category = data.get('category')
        surveyTitle.save()

        return HttpResponse(status=204)


def keyword_match(titles, categories, semantic_match=True):
    if type(titles) is not list:
        titles = [titles]
    if type(categories) is not list:
        categories = [categories]

    lang = "ko"
    dct = {"sentences": titles, 'reference_keywords': categories, "lang": lang, "semantic_match": semantic_match}

    r = requests.post(
        url='https://a197b78a-45f9-4706-bce6-d668859e7e37.api.kr-central-1.kakaoi.io/ai/nlp/fa3247354be345afb29873feeba54045',
        headers={'x-api-key': '2d8babd29a174e059f936b7d5bbd9422',
                 'Content-Type': 'application/json'},
        data=json.dumps(dct)
        )

    data = json.loads(r.text)

    max_score = -1
    target_detail = {"reference_keyword": "", "matched_keyword": "", "score": -1}
    # 에러 코드 처리 부분 추가하면 좋을듯
    for detail in data.get("result").get("details"):
        cur_score = detail.get('score')
        if cur_score > max_score:
            max_score = cur_score
            target_detail = detail.copy()

    return target_detail


def extract_keyword(title):
    sentences = [
        title
    ]
    lang = "ko"
    dct = {"sentences": sentences, "lang": lang}

    r = requests.post(
        url='https://ea8d8356-1901-482d-ab95-744f6bc5503b.api.kr-central-1.kakaoi.io/ai/nlp/0cf9668c030b4a5d9bed1c0567e0e2a1',
        headers={'x-api-key': '2724722f67ad200e792334b9c443fb75',
                 'Content-Type': 'application/json'},
        data=json.dumps(dct)
        )
    return r.text
