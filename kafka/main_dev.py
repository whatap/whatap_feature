import requests, json
import logging

# Enable debug logging for requests

# from http.client import HTTPConnection, HTTPSConnection
# HTTPConnection.debuglevel = 1
# HTTPSConnection.debuglevel = 1


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
document_primary_keys=["id", "type","data"]
def getFeatures(url_prefix=url_prefix, url_path = "/admin/api/feature/list", url_cookie=url_cookie):
    url_getfeature = "{}{}".format(url_prefix, url_path)
    headers={"cookie":url_cookie}
    r = requests.get(url_getfeature, headers=headers)

    features = r.json()['data']
    #print(features)
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

def createFeature(url_prefix=url_prefix, url_path = "/admin/api/feature/create", url_cookie=url_cookie):

    metaJson = getMetaJson()
    # metaJson = """{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}"""
    installationJson = getInstallJSON()
    body = {
    "platform":"INFRA",
    "textKey":"KAFKA",
    "name":"KAFKA",
    "description":"KAFKA BETA RC 0604",
    "status":"open",
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

def updateFeature(featureId=20, url_prefix=url_prefix, url_path = "/admin/api/feature/update", url_cookie=url_cookie):
    metaJson = getMetaJson()
    installationJson = getInstallJSON()
    
    
    #installationJson="""{\"ja\":{\"title\":\"設置前の注意事項\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntuサポートバージョン\",\"version\":\"12.04以上\"},{\"type\":\"support-version\",\"title\":\"Kafka サポートバージョン\",\"version\":\"Apache Kafka 3.x以降\"},{\"type\":\"support-version\",\"title\":\"OS対応バージョン\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"オペレーティングシステムのアーキテクチャ\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"アクセスキーの確認\",\"description\":\"アクセスキーは、ワタップサービスを有効にするための一意のIDです。\\n{get_license_feature}\"},{\"title\":\"インストールスクリプトの生成\",\"boxes\":[{\"prepend\":\"KAFKAがインストールされているサーバーにスクリプトを生成するには、以下のコマンドを実行してください。\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"以下のコマンドを実行してください。\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"モニタリングを始める\",\"description\":\"KAFKAでJolokiaエージェントを設定するには、以下のコマンドを実行して再起動してください。\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]},\"en\":{\"title\":\"Precautions before installation\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntu supported versions\",\"version\":\"12.04 or higher\"},{\"type\":\"support-version\",\"title\":\"Kafka supported versions\",\"version\":\"Apache Kafka 3.x or higher\"},{\"type\":\"support-version\",\"title\":\"OS supported version\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"Operating system architecture\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"Check access key\",\"description\":\"The access key is a unique ID for activating the WhaTap service.\\n{get_license_feature}\"},{\"title\":\"Generate installation script\",\"boxes\":[{\"prepend\":\"Run the command below to create a script on the server where KAFKA is installed.\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"Run the command below.\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"Start monitoring\",\"description\":\"To set up the Jolokia agent in KAFKA, run the command below and then restart.\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]},\"ko\":{\"title\":\"설치 전 유의사항\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntu 지원 버전\",\"version\":\"12.04 이상\"},{\"type\":\"support-version\",\"title\":\"Kafka 지원 버전\",\"version\":\"Apache Kafka 3.x 이상\"},{\"type\":\"support-version\",\"title\":\"OS 지원 버전\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"운영체제 아키텍처\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"액세스 키 확인\",\"description\":\"액세스 키는 와탭 서비스 활성화를 위한 고유 ID입니다.\\n{get_license_feature}\"},{\"title\":\"설치 스크립트 생성\",\"boxes\":[{\"prepend\":\"KAFKA가 설치된 서버에 스크립트를 생성하기 위해 아래 명령어를 실행하세요.\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"아래 명령어를 실행하세요.\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"모니터링 시작하기\",\"description\":\"KAFKA에 Jolokia 에이전트 설정을 위해 아래 명령어를 실행 후 재시작하세요.\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]}}"""
    # f = open('test.json','w')
    # f.write(json.dumps(json.loads(installationJson), indent=4))
    # f.close()
    body = {
    "id": featureId,
    "platform":"INFRA",
    "textKey":"KAFKA_HSNAM_NINE",
    "name":"KAFKA HSNAM NINE",
    "description":"FEATURE KAFKA HSNAM 0603 TEST 4",
    "status":"open",
    "document":[]
    }

    body = {
    "id": featureId,
    "platform":"INFRA",
    "textKey":"KAFKA_RC_ONE_PONE",
    "name":"KAFKA BETA RC",
    "description":"KAFKA BETA RC 0604-1",
    "status":"open",
    "document": [
    ]}

    eventLookup = {name: eventDoc for (_, name, eventDoc) in getEventDocs()}
    dashboardLookup = {json.loads(dashboardDoc)['name']: dashboardDoc for dashboardDoc in getDashboardDocs()}

    for feature in getFeatures():
        if featureId == feature['id']:
            body = feature
            documents =body['document']
            processedDocs = []
            for doc in documents:
                if doc['type'] == 'installation':
                    doc['data'] = installationJson
                    processedDocs.append(doc)
                elif doc['type'] == 'event':
                    name = doc['name']
                    if name in eventLookup:
                        doc['data'] = eventLookup[name]
                        processedDocs.append(doc)
                # elif doc['type'] == 'dashboard':
                #     name = doc['name']
                #     if name in dashboardLookup:
                #         doc['data'] = dashboardLookup[name]
                #         processedDocs.append(doc)

            # body['document'].append({"id":63,"type":"installation", "data": installationJson, "single":True})
            body['document']=processedDocs
            #body['name']="KAFKA"
            #{"id":37,"type":"meta", "data": metaJson, "single":True},
            #{"id":38,"type":"installation", "data": installationJson, "single":True}
            #
            # for dashboardDoc in getDashboardDocs():
            #     body['document'].append({"type":"dashboard", "name":json.loads(dashboardDoc)['name'], "data":json.dumps({}), "single":False})

            # for (docid, dashboardDoc) in getDashboardDocEx():
            #     if docid:
            #         body['document'].append({"id": docid, "type":"dashboard", "name":json.loads(dashboardDoc)['name'], "data":dashboardDoc, "single":False})
            #     else:
            #         body['document'].append({ "type":"dashboard", "name":json.loads(dashboardDoc)['name'], "data":dashboardDoc, "single":False})
                
            # for (docid, name, eventDoc) in getEventDocs():
            #     if docid:
            #         body['document'].append({"id": docid, "type":"event", "name":name, "data":eventDoc, "single":False})
            #     else:
            #         pass
            #         body['document'].append({"type":"event", "name":name, "data":"[]", "single":False})
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
    #createFeature()
    # updateFeature(featureId=31)
    for feature in getFeatures():
        pass
        #print(feature)
    
    #updateAllFeatureClose()

def writeMeta():
    with open('meta.json','w') as f:
        f.write(getMetaJson())
    body = {
        "platform":"INFRA",
        "textKey":"KAFKA",
        "name":"KAFKA",
        "description":"KAFKA BETA RC 0604",
        "status":"open"
        }
    with open('main.json','w') as f:
        f.write(json.dumps(body))


if __name__ == '__main__':
    main()
    #writeMeta()
