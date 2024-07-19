import requests, json
import logging

# Enable debug logging for requests

from http.client import HTTPConnection, HTTPSConnection
HTTPConnection.debuglevel = 1
HTTPSConnection.debuglevel = 1


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error reading file: {e}"


url_prefix="https://preview.whatap.io"
url_cookie='ch-veil-id=ba9232c5-a727-4859-9bd2-c4f97a893c0b; _fbp=fb.1.1648201957567.478146268; experimentation_subject_id=IjY2YmEwMDY2LTk3YzktNGY1MC1iOThkLTMwYmI1NzVlN2UxZiI%3D--9d0bd7c5858261234bd39fa8f46a3ffa0e763678; _hjSessionUser_2220606=eyJpZCI6ImM0ODllNjZmLWY3YjctNTQ4MS04YzAxLWQ4YjM5ODgyYWZkNiIsImNyZWF0ZWQiOjE2NTMyOTczNjMwNjUsImV4aXN0aW5nIjp0cnVlfQ==; _clck=18cku4|2|fdd|0|1254; whatap_user_id_26752=x4upodnj8olrq; whatap_is_page_load_complete=true; __stripe_mid=05dd090b-eddc-4fc2-8554-5d7904633b52e998a0; _fbc=fb.1.1703036079829.IwAR0S4VgP76QP648XbPy9ogDMtLcPeGXcILH0FWR7CnZvHFD265iwuFyuA34; AMP_MKTG_003c057580=JTdCJTdE; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2Fa4ce33ca=session_7c6bdc55-2314-4640-a826-1c7e0edc8cda; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F1fe6e75f=session_28c38905-1e95-45f0-898f-087410f9c73c; _gcl_au=1.1.613590776.1711691839; AMP_MKTG_503bad153d=JTdCJTdE; AMP_MKTG_6a8d411e88=JTdCJTdE; _ga_NR722KYGXH=GS1.1.1714352039.456.0.1714352142.60.0.0; _ga=GA1.1.1310047645.1648201957; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F08846565=session_c6858d6a-c06a-4970-ad1c-94210b75e8bf; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F1f88557a=session_0695c3aa-e97d-4d52-9973-d1f653fd542d; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; whatap_user_id_302=xqfbgpavn3437; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F4ec1e762=session_a8f7b40b-a5bc-47c3-b77c-750dff46bf8a; _whatap.p0={%22viewType%22:%22grid%22}; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2Fc0f45a62=session_f10472be-c3ec-4892-a673-9ace5e853909; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F8106036c=session_06229981-0168-4d3c-83f9-28903f13d946; AMP_MKTG_5b5bc63c68=JTdCJTdE; AMP_5b5bc63c68=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1YjczMDM4Yy1jNWM1LTRjYjEtYmM0NS1hNjdiN2U0YTE5MDUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE4ODczMzUwMDkyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxODg3MzM1NTYzOSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMyUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMiU3RA==; _ga_BBQ5SJJP5G=GS1.1.1718930199.2.0.1718930199.0.0.0; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477=session_8102fea8-bd81-4613-a01b-80ceadf0fa54; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F95cda199=session_8102fea8-bd81-4613-a01b-80ceadf0fa54; AMP_6a8d411e88=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlY2M4YWE0YS0yYzUzLTQyZDEtOGJkNS00NDc5YTY4YTQ4ZWUlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJoc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg5NDIxNjc0NTMlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4OTQyMjI4NTg1JTJDJTIybGFzdEV2ZW50SWQlMjIlM0ExMDE4MiU3RA==; _ga_E46TQ5VSCT=GS1.1.1718950562.518.1.1718950716.60.0.2014638053; AMP_003c057580=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI5MTUxM2VhOS1mYmRlLTQxYjUtYTExMS0xM2ViYTE3NWZhZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJoc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg5NDg2OTU1MjUlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4OTUwNzk3MTk4JTJDJTIybGFzdEV2ZW50SWQlMjIlM0ExNzY4MyU3RA==; whatap_sesion_max_expired_302=Fri, 21 Jun 2024 10:36:57 GMT; whatap_session_id_302=z24mrq0jnhpdk5; whatap_is_collect_session_302=true; cf_clearance=.vd1K4JgzVf7dsL.VKlNuF_LSxuGkuO7zuj2xOd3zfU-1718951818-1.0.1.1-X0q0BjGd1u2vGHl34LfiSXnP9ooo9gs8vNalcGP0VYtbbIQBenAfScNL6iuVZ67k9lO7jq9ABz1g0NRSYzCnaQ; JSESSIONID=MjA3N2FiM2ItM2M3NS00ZGM4LTkzOWQtMzJkZGMzNmE5YWMw; lang=ko; wa="Wb7VJsswGYB1v+pgMb9JbT5HQsVVaaPXWqnL8JMIVAMe37Q3E7M/GyBx0UkHPoJxDLdHHsU9a8eKlcYtUiwYSg=="; lang=ko; whatap_is_page_load_complete_302=true; AMP_503bad153d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2Mzg2YjRhOS00YzIxLTQ1MmQtYTYyMi00Y2NiNDMyN2E4MzAlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzYV9oc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg5NTE4MTgzOTUlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4OTUxODI1MzgwJTJDJTIybGFzdEV2ZW50SWQlMjIlM0EzNDQ4JTdE; AWSALBAPP-0=AAAAAAAAAADAUEcKntJLTkchylkyp7CC23cRBhCR8QA8u1uFgfw2QPPS+NIHsFe0kCY8wsiW9qJbNdHCxWA6ajrXjMJeuxJQGcMEgvUQCF+1ric/CGy1+2tqQzpYIcNKCQ7g3LluuOL1wzg='

#url_prefix="https://dev.whatap.io"
#url_cookie='cookie: ch-veil-id=ba9232c5-a727-4859-9bd2-c4f97a893c0b; _fbp=fb.1.1648201957567.478146268; experimentation_subject_id=IjY2YmEwMDY2LTk3YzktNGY1MC1iOThkLTMwYmI1NzVlN2UxZiI%3D--9d0bd7c5858261234bd39fa8f46a3ffa0e763678; _hjSessionUser_2220606=eyJpZCI6ImM0ODllNjZmLWY3YjctNTQ4MS04YzAxLWQ4YjM5ODgyYWZkNiIsImNyZWF0ZWQiOjE2NTMyOTczNjMwNjUsImV4aXN0aW5nIjp0cnVlfQ==; _clck=18cku4|2|fdd|0|1254; _fbc=fb.1.1703036079829.IwAR0S4VgP76QP648XbPy9ogDMtLcPeGXcILH0FWR7CnZvHFD265iwuFyuA34; whatap_is_page_load_complete=true; pll_language=ko; AMP_MKTG_003c057580=JTdCJTdE; whatap_user_id_401=hsnam@whatap.io; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2Fa4ce33ca=session_7c6bdc55-2314-4640-a826-1c7e0edc8cda; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F1fe6e75f=session_28c38905-1e95-45f0-898f-087410f9c73c; _gcl_au=1.1.613590776.1711691839; AMP_MKTG_503bad153d=JTdCJTdE; AMP_MKTG_6a8d411e88=JTdCJTdE; _ga_NR722KYGXH=GS1.1.1714352039.456.0.1714352142.60.0.0; _ga=GA1.1.1310047645.1648201957; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2Fc0f45a62=session_74d07b35-f0a4-44f9-be2d-eacb74779208; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F08846565=session_c6858d6a-c06a-4970-ad1c-94210b75e8bf; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F1f88557a=session_0695c3aa-e97d-4d52-9973-d1f653fd542d; _whatap.p0={%22viewType%22:%22grid%22}; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F8106036c=session_f2a9825b-e193-43d2-b254-45c6be31ec38; person=%257B%2522EVENT_ALERT_POPUP%2522%253Afalse%257D; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F95cda199=session_21c690cf-862f-487e-afc6-71e75de2f91c; AMP_6a8d411e88=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIzMGE2NTQ5Ny1kZDUxLTQ5YWEtYjNiYS1lMGIxZjBiMGFkOTElMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzYV9oc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg2Njg4NTk3NTMlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4NjY4OTA0MDk4JTJDJTIybGFzdEV2ZW50SWQlMjIlM0ExMDEyMyU3RA==; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F4ec1e762=session_a8f7b40b-a5bc-47c3-b77c-750dff46bf8a; cf_clearance=oEljr_O9XxLhnbAtMwLBFLazbmGYKCS9XZB73VwLxT0-1718681596-1.0.1.1-4tmPbC5MvNOUmPawuGZATqWxBHypnhi18X41fiBWvSQYAEw20xcAIfq0VuwhYDK5rTSFb9Wbr6me3Oziwp3pGQ; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477=session_1ec88ca4-713d-4b8e-8a46-c3a6d4b95be9; AMP_503bad153d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiMmM4NWUxOS1lNmE3LTRkMDQtOTU2ZC01NzI1ZWE4YTA0NzYlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzYV9oc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg2ODE2MDE2OTclMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4NjgzMzQzMTY1JTJDJTIybGFzdEV2ZW50SWQlMjIlM0EzNDMwJTdE; _ga_E46TQ5VSCT=GS1.1.1718684435.512.1.1718684451.44.0.1812940020; whatap_session_id_401=z6g3c1fim606k7; whatap_session_max_expired_401=Tue, 18 Jun 2024 08:32:09 GMT; whatap_session_collect_type_401=2; JSESSIONID=OGM0NTI1MjItMGMyNy00NGM0LWI3NGItMDQwNWY0OGVhOWMy; lang=ko; wa=cuLqX8FQnme1bApaM9jLvfOdBwygWOJsfATD7KPZe6HrHBlz46xbmJ8ntKn4DtQn; lang=ko; whatap_is_page_load_complete_401=true; AMP_003c057580=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxMTE4NmI3MC1mNGRmLTQ5YWEtYmQ5ZC00NWZiZGMxY2Y2YTElMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzYSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTg2ODUxMjk2NjAlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE4Njg1MzUzMDkxJTJDJTIybGFzdEV2ZW50SWQlMjIlM0ExNzUwNiU3RA==; AWSALBAPP-0=AAAAAAAAAACKxBbGgw7l0iXbpf7T09dkCRZQlkDPiN42L4ME66HqvnAwDJcTnUHJJYvLtRAs8pEhbEzpICe4VRBNKKpnTMBY2M19pHxD3mJYiFmmlpgUEyC/GjimLLu6vZOIlDAD8/HlUcA='


feature_primary_keys=["id","name","textKey","productType","platform",  "description", "status"]
document_primary_keys=["id", "type"]
def getFeatures(url_prefix=url_prefix, url_path = "/admin/api/feature/list", url_cookie=url_cookie):
    url_getfeature = "{}{}".format(url_prefix, url_path)
    headers={"cookie":url_cookie}
    r = requests.get(url_getfeature, headers=headers)

    features = r.json()['data']
    for feature in features:
        print("="*40)
        for k in feature_primary_keys:
            print(k,":", feature[k])
        docs = feature['document']
        for doc in docs:
            print("-"*40)
            for kk in document_primary_keys:
                print(kk,":", doc[kk])
        yield feature

import json

def getMetaJson():
    metadata = {
        "desc": {
            "icon": "kafka",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.",
                "ja": "データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。",
                "en": "Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights."
            }
        },
        "releaseEnvs": ["DEV", "PREVIEW", "SERVICE"]
        #"releaseEnvs": ["DEV"]
    }

    return json.dumps(metadata)

def getInstallJSON():

    return json.dumps(json.loads(read_file("installation.json")))

def getEventDocs():
    events = json.loads(read_file("event_composite_metrics.json"))
    processed_events = []
    for event in events:
        process_event = {k: v for k, v in event.items() if k != "id" and k != "receiver" and k != "event_level_text"}
        process_event['event_level'] = 30
        processed_events.append(process_event)
    f = open('event_doc.json','w')
    f.write(json.dumps(processed_events, indent=2))
    f.close()
    
    return [(80, "COMPOSITE_METRICS", json.dumps(processed_events)),]

def getDashboardDoc( dataDoc):
    return {
        "type": "dashboard",
        "data": dataDoc,
        "single": False
    }


def getDashboardDocs():

    return [json.dumps(json.loads(read_file("dashboard_default.json"))),
            json.dumps(json.loads(read_file("dashboard_broker.json"))),
            json.dumps(json.loads(read_file("dashboard_request.json")))]


def getDashboardDocEx():

    # return [(52,read_file("dashboard_default.json")),]
    return [  (65, json.dumps(json.loads(read_file("dashboard_default.json")))),
            (66, json.dumps(json.loads(read_file("dashboard_broker.json")))),
             (67, json.dumps(json.loads(read_file("dashboard_request.json"))))]


def createFeatureDev(url_prefix=url_prefix, url_path = "/admin/api/feature/create", url_cookie=url_cookie):

    metaJson = getMetaJson()
    # metaJson = """{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}"""
    installationJson = getInstallJSON()
    body = {
    "platform":"INFRA",
    "textKey":"KAFKA_RC_ONE_DEV",
    "name":"KAFKA",
    "description":"KAFKA BETA RC 202406",
    "status":"beta",
    "document": [
	    {"type":"meta", "data": metaJson, "single":True},
	    {"type":"installation", "data": installationJson, "single":True},
	    
    ]}

    for (_, name, eventDoc) in getEventDocs():
        body['document'].append({"type":"event","name":name, "data":eventDoc, "single":False})

    for dashboardDoc in getDashboardDocs():
        body['document'].append({"type":"dashboard","name":json.loads(dashboardDoc)['name'], "data":dashboardDoc, "single":False})

    url_create_feature="{}{}".format(url_prefix, url_path)

    headers={"cookie":url_cookie}
    r = requests.post(url_create_feature, headers = headers, json = body)

    for k, v in r.json().items():
        print(k, json.dumps(v)[:10],"...")


def createFeature(url_prefix=url_prefix, url_path = "/admin/api/feature/create", url_cookie=url_cookie):

    metaJson = getMetaJson()
    # metaJson = """{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}"""
    installationJson = getInstallJSON()
    body = {
    "platform":"INFRA",
    "textKey":"KAFKA_RC_ONE",
    "name":"KAFKA",
    "description":"KAFKA BETA RC 202406",
    "status":"beta",
    "document": [
	    {"type":"meta", "data": metaJson, "single":True},
	    {"type":"installation", "data": installationJson, "single":True},
	    
    ]}

    for (_, name, eventDoc) in getEventDocs():
        body['document'].append({"type":"event","name":name, "data":eventDoc, "single":False})

    for dashboardDoc in getDashboardDocs():
        body['document'].append({"type":"dashboard","name":json.loads(dashboardDoc)['name'], "data":dashboardDoc, "single":False})

    url_create_feature="{}{}".format(url_prefix, url_path)

    headers={"cookie":url_cookie}
    r = requests.post(url_create_feature, headers = headers, json = body)

    for k, v in r.json().items():
        print(k, json.dumps(v)[:10],"...")


def createFeatureSimple(url_prefix=url_prefix, url_path = "/admin/api/feature/create", url_cookie=url_cookie):
    body = {
    "platform":"INFRA",
    "textKey":"KAFKA_HSNAM_FIVE",
    "name":"KAFKA_HSNAM_FIVE",
    "description":"FEATURE KAFKA HSNAM 0527 TEST 5",
    "status":"open"
    }


    url_create_feature="{}{}".format(url_prefix, url_path)

    headers={"cookie":url_cookie}
    r = requests.post(url_create_feature, headers = headers, json = body)
    resp = r.json()
    for k, v in resp.items():
        print(k, v)

def updateFeature(featureId=1, url_prefix=url_prefix, url_path = "/admin/api/feature/update", url_cookie=url_cookie):
    installationJson = getInstallJSON()
    eventLookup = {name: eventDoc for (_, name, eventDoc) in getEventDocs()}
    dashboardLookup = {json.loads(dashboardDoc)['name']: dashboardDoc for dashboardDoc in getDashboardDocs()}

    feature = None
    for f in getFeatures():
        fid = f['id']
        if fid == featureId:
            feature = f
            break
    if not feature:
        print("feature not found")
        return
    documents = []

    for doc in feature['document']:
        docType = doc['type']
        if "installation" == docType:
            doc['data'] = installationJson
            documents.append(doc)
        elif doc['type'] == 'event':
            name = doc['name']
            if name in eventLookup:
                doc['data'] = eventLookup[name]
                documents.append(doc)
        elif doc['type'] == 'dashboard':
            name = doc['name']
            if name in dashboardLookup:
                doc['data'] = dashboardLookup[name]
                documents.append(doc)
    
    if not documents:
        print("installation not found")
        return    
    feature['document'] = documents
    from pprint import pprint

    pprint(feature)
    body = feature
    url_create_feature="{}{}".format(url_prefix, url_path)

    headers={"cookie":url_cookie}
    r = requests.post(url_create_feature, headers = headers, json = body)
    print(r.text)

def updateAllFeatureClose(url_prefix=url_prefix, url_update_path = "/admin/api/feature/update", url_cookie=url_cookie):
    url_update_feature="{}{}".format(url_prefix, url_update_path)
    for feature in getFeatures():
        textKey = feature['textKey']
        if textKey.startswith('KAFKA_'):
            url_udpate_feature="{}{}".format(url_prefix, url_update_path)
            feature['status']='closed'
            headers={"cookie":url_cookie}
            r = requests.post(url_update_feature, headers = headers, json = feature)

def main():
    print("hello world")
    #createFeatureDev()
    featureId=1
    updateFeature(featureId=featureId)
    # for f in getFeatures():
    #    pass
    #    if f['id'] == featureId:
    #        print(list(filter(lambda x: x['type']=='installation', f['document'])))
    #updateAllFeatureClose()

if __name__ == '__main__':
    main()

