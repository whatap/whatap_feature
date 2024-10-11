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


url_prefix="https://dev.whatap.io"
url_cookie='AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; whatap_user_id_401=x2tc2asm7ls1jp; AMP_MKTG_003c057580=JTdCJTdE; AMP_MKTG_6a8d411e88=JTdCJTdE; _ga=GA1.1.354235464.1716168272; AMP_MKTG_503bad153d=JTdCJTdE; AMP_503bad153d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiZWI1MTUyZS02MmMyLTRmMDYtYTc0Ny1kNmU1NDdjNDNjM2UlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJoc25hbSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTYxOTUwMzcyODAlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE2MTk1MjIxMjg1JTJDJTIybGFzdEV2ZW50SWQlMjIlM0ExMCU3RA==; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F8106036c=session_5e21f4bb-fbb9-42cb-8370-d69f1299834f; lang=ko; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2F4ec1e762=session_cd5401cf-11c1-4636-89b3-59fb154f36d5; person=%257B%2522EVENT_ALERT_POPUP%2522%253Afalse%257D; _whatap.p0={%22viewType%22:%22grid%22}; _ga_E46TQ5VSCT=GS1.1.1716510567.4.0.1716510567.60.0.911121871; cf_clearance=R_RmAnfI_SY1wL4cmNQLXKYe_BOg3uDVjCX1uL769Qs-1716530494-1.0.1.1-hjBNi6fsJ.9S_YE22JJYa07hRwcAy8BxHWOH7Y_ahIZ1dg6IBZHKSNwp6GpkyTriR.5PnxEJzZZwmT7Itux9OQ; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477%2Fc0f45a62=session_333b1a0e-d5aa-4be1-9c26-98b03592bfdc; AMP_6a8d411e88=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1ZTExYTExZS0zYzc2LTRmMDYtOGIxOS05YmFjNTRjZGY5MzMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJkZW1vJTQwd2hhdGFwLmlvJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTcxNjUzMDQ5NDg2NiUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3MTY1MzA1NjA0MDklMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTE1NiU3RA==; whatap_session_id_401=z4faf9frum0v27; whatap_session_max_expired_401=Mon, 27 May 2024 08:15:07 GMT; whatap_session_collect_type_401=2; crisp-client%2Fsession%2F9a0c342f-a5b1-4c4a-a22f-92c7b4b9b477=session_c8ca3dad-84ea-4f23-99ad-02cc45a29439; JSESSIONID=M2U2NzQ1NjUtYWIwMy00YTU5LWJhMjMtNzE5MzFmNDU4Njcy; wa=cuLqX8FQnme1bApaM9jLvbctJlmQHktMqYknaFxecSYK9cdWMq+CSZ1ftxKGJtiZ; whatap_is_page_load_complete_401=true; AMP_003c057580=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1MWNkOThhYy0zYjc1LTQ5NjEtYmFiNC0zYTdmZjg1ZDliZDIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzYSU0MHdoYXRhcC5pbyUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MTY3ODMzMDc5NDQlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzE2NzgzNDEyNDQ0JTJDJTIybGFzdEV2ZW50SWQlMjIlM0EyMDUlN0Q=; AWSALBAPP-0=AAAAAAAAAACM3pNmukyBopCVaGIIGnJw9BQ5RzGCmHE06wB5nTGHuzRRbjsw08rXn+S+MGagyzEM65uZtCQIp7Xqf6nzMGfoEs6qKVW9HAw1GlPOaYwuqlw/6aBEmv3FjcInBRa3AHysj78='

#url_prefix="http://127.0.0.1:8080"
#url_cookie='''whatap_user_id_29812=z67itbqbe1h1j2; whatap_is_page_load_complete=true; whatap_user_id=z7j4gi9oa3i2o9; WHATAP=xsjm55d; csrftoken=Oj8iy7frzzcovDXLrSHnk1z9z98BQTjMnIhyrWj1tQGwXwdBNibfSIn6gas0MEnO; whatap_user_id_386=z2qd3fd1nqu5n0; lang=en; pll_language=en; whatap_user_id_1715=z7jd23s9dpoddl; whatap_is_page_load_complete_1715=true; sessionid=ocmchfkm6bk2ngumc9ydng3l218vmres; JSESSIONID=pI8CiYfDYnelIu4PPyjwHGTYY8NRKEGJlWUpWFQ2; wa="W/Kz829oWnH9XO5deG5iPZ/Qv6MNpCzl7sjXS6WJvXcSVg95ntzdYjbMH3v1wo2obCWQLMub8No="' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin'''

feature_primary_keys=["id","name","textKey","productType","platform",  "description", "status"]
document_primary_keys=["id", "type"]
def getFeatures(url_prefix=url_prefix, url_path = "/admin/api/feature/list", url_cookie=url_cookie):
    url_getfeature = "{}{}".format(url_prefix, url_path)
    headers={"cookie":url_cookie}
    r = requests.get(url_getfeature, headers=headers)

    features = r.json()['data']
    print(features)
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
            "icon": "vsphere",
            "pricingUrl": "https://www.whatap.io/ko/pricing/#server-space",
            "summary": {
                "ko": "vCenter를 통해 서버 가상화 환경을 효율적으로 관리하세요. 실시간 모니터링과 강력한 관리 도구로 서버의 상태를 한눈에 파악하고, 문제 발생 시 빠르게 대응할 수 있습니다. 이제 vCenter로 IT 인프라를 최적화하고 운영 효율성을 극대화하세요.",
                "en": "Efficiently manage your virtualized server environment with vCenter. With real-time monitoring and powerful management tools, you can easily assess server health and respond quickly to any issues. Optimize your IT infrastructure and maximize operational efficiency with vCenter today.",
                "ja": "vCenterを使用して仮想化されたサーバー環境を効率的に管理しましょう。リアルタイムモニタリングおよび強力な管理ツールにより、サーバーの健全性を簡単に評価し、問題が発生した場合には迅速に対応できます。vCenterでITインフラを最適化し、運用効率を最大限に引き上げてください。",
            }
        },
        "releaseEnvs": ["DEV", "PREVIEW", "SERVICE"]
        #"releaseEnvs": ["DEV"]
    }

    return json.dumps(metadata)

def getInstallJSON():

    return json.dumps(json.loads(read_file("installation.json")))

def getEventDocs():
    
    #return []
    return [(None, "METRICS", read_file("event-rules.json")),]

def getDashboardDoc( dataDoc):
    return {
        "type": "dashboard",
        "data": dataDoc,
        "single": False
    }


def getDashboardDocs():

    return [json.dumps(json.loads(read_file("vHost Performance Overview.json"))),
           json.dumps(json.loads(read_file("VMGuest Performance Overview.json"))),
           json.dumps(json.loads(read_file("VMware Datastore.json"))),
           json.dumps(json.loads(read_file("VMware Hosts.json"))),
           json.dumps(json.loads(read_file("VMware Performance Overview.json"))),
           json.dumps(json.loads(read_file("VMware VMs.json"))),
           json.dumps(json.loads(read_file("VMware Summary.json"))),
           ]


def createFeature(url_prefix=url_prefix, url_path = "/admin/api/feature/create", url_cookie=url_cookie):

    metaJson = getMetaJson()
    # metaJson = """{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}"""
    installationJson = getInstallJSON()
    body = {
    "platform":"INFRA",
    "textKey":"VCENTER_DEV_ONE",
    "name":"vCenter",
    "description":"vCenter BETA RC 0604",
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

def updateFeature(featureId=1, url_prefix=url_prefix, url_path = "/admin/api/feature/update", url_cookie=url_cookie):
    metaJson = getMetaJson()
    installationJson = getInstallJSON()
    feature = None
    for f in getFeatures():
        fid = f['id']
        if fid == featureId:
            feature = f
            break
    if not feature:
        print("feature not found")
        return
    documents = [
        
    ]

    for (_, name, eventDoc) in getEventDocs():
        documents.append({"type":"event","name":name, "data":eventDoc, "single":False})

    for doc in feature['document']:
        docType = doc['type']
        if "installation" == docType:
            doc['data'] = installationJson
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

def addEvent(pcode=0):
    
    metrics = []
    for event in json.loads(read_file('event_doc2.json') ):
        # del ev['id']
        process_event = {k: v for k, v in event.items() if k != "id" and k != "receiver" and k != "event_level_text"}
        # process_event['event_level'] = 30
        process_event['eventLevel'] = 30
        
        metrics.append(process_event)
        pass
    events = {"METRICS": metrics}
    body = {'productType':"SMS", 'platform':"INFRA", 'events':events}
    
    r = requests.post(f"http://ec2-15-165-146-117.ap-northeast-2.compute.amazonaws.com:7710/feature/pcode/{pcode}/event/add",  json=body)
    print(r.text)
    

def addEvent2(pcode=109):
    
    metrics = []
    for event in json.loads(read_file('event_doc2.json') ):
        # del ev['id']
        process_event = {k: v for k, v in event.items() if k != "id" and k != "receiver" and k != "event_level_text"}
        process_event['eventLevel'] = 30
        
        metrics.append(process_event)
        pass
    events = {"METRICS": metrics}
    body = {'productType':"SMS", 'platform':"INFRA", 'events':events}
    
    r = requests.post(f"http://localhost:7710/feature/pcode/{pcode}/event/add",  json=body)
    print(r.text)
        

def writeMeta():
    with open('meta.json','w') as f:
        f.write(getMetaJson())
    body = {
    "platform":"INFRA",
    "textKey":"VCENTER_DEV_TWO",
    "name":"vCenter",
    "description":"vCenter BETA RC 1004",
    "status":"beta"}
    with open('main.json','w') as f:
        f.write(json.dumps(body))


def main():
    print("hello world")
    createFeature()
    # updateFeature(featureId=23)
    # for _ in getFeatures():
    #      pass
    
    #updateAllFeatureClose()

if __name__ == '__main__':
    #main()
    writeMeta()
    #addEvent(pcode=2924)
    # addEvent2()