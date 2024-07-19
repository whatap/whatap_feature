# Feature 관리 가이드

- Contents

## 개요

 Feature API 를 사용하여, Feature 를 추가하는 방법과 Feature 관리 흐름에 대해 설명합니다.

## 참조

- [Admin API Sig.](https://www.notion.so/Feature-Admin-API-38088a20dad247e68b28622747c62ab9?pvs=21)
- [User API Sig.](https://www.notion.so/01-Feature-3eb6576785954ed79964d5f1099958f5?pvs=21)

<aside>
💡 API 호출은 apiTester 를 이용한 예시를 제공합니다. postman 과 같은 api 테스트 툴을 사용하여도 상관 없습니다.

</aside>

### APITester 사용하기

- admin 권한을 가진 계정(ex- sa@whatap.io)으로 로그인합니다.
- ~/v2/account/apiTester 페이지로 접근합니다.
    - ex) dev 환경 - [https://dev.whatap.io/v2/account/apiTester](https://dev.whatap.io/v2/account/apiTester)
- 호출하고자하는 api 의 method, path 등 값을 입력하고 ‘요청’을 누른 뒤, 결과를 확인합니다.
    - ex) 피처 목록 조회 admin api 호출
        
        ![Screen Shot 2024-05-08 at 12.26.10 AM.png](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Screen_Shot_2024-05-08_at_12.26.10_AM.png)
        

### JSON 정보를 stringify 처리하기

1. 브라우저 콘솔 창 켜기
    - 브라우저에서 개발자 도구를 열어 아래의 콘솔을 사용합니다.
        
        ![Untitled](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Untitled.png)
        
2. 변수 선언
    - var 변수명 = 내용
        
        ![Untitled](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Untitled%201.png)
        
    
    변수명은 아무거나 사용해도 상관 없습니다. 내용을 붙여넣기 하고 Enter 입력
    
3. `JSON.stringify(변수명)` 입력
    
    ![Untitled](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Untitled%202.png)
    
4. 결과 값에서 우클릭해서 “문자열을 JSON 리터럴로 복사” 클릭
    
    ![Untitled](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Untitled%203.png)
    
5. 완료: 아래와 같은 문자열이 생성되었다면 stringify 완료
    
    ```json
    "{\"layout\":{\"type\":\"FIXED\",\"monitor\":{\"x\":3,\"y\":3}},\"pcodes\":[24],\"option\":{\"stime\":1713253874544,\"etime\":1713254474544,\"timeAction\":\"LIVE_10MIN\"}}"
    ```
    

## 피처 조회하기

### 목록 조회

- 기존에 생성되어있던 피처 목록 및 상태 등을 확인하려면 목록 조회 api를 호출합니다.
    - Signature
        - [GET] **/admin/api/feature/list**
        - query-params: parameter 없이 조회 시 전체 리스트를 반환
            - List<String> productType
            - List<String> platform
            - List<String> textKey
            - List<String> status
        - response
            - response body
                
                ```json
                // response body
                {
                    "msg": "success",
                    "code": 200,
                    "data": Array<FeatureListItem>, //아래에 데이터 설명 참고
                    "ok": true
                }
                
                ```
                
            - FeatureListItem Object
                
                ```json
                {
                  "id": 9,
                  "productType": "APM",
                	"platform": "GO",
                	"textKey": "KAFKA", // feature 식별을 위한 고유값(중복 불가)
                	"name": "INFRA-TEST",  // display name. UI 에서는 해당 값으로 표시됩니다.
                	"description": "FEATURE INFRA TEST", // UI에 표시되지 않는 메타 정보
                	"status": "beta", // "open" 인 경우에만 서비스에 노출됩니다.
                	// 관리자용 조회 API 에서는 모든 document를 조회합니다.
                	// 사용자용 조회 API 에서는 document.meta 정보만 조회합니다. 
                	"document": [
                      {
                          "id": 6,
                          "type": "event",
                          "name": "COMPOSITE_LOG",
                          "data": "[{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_2xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"AppLog\",\"$include_filter_values\":\"status_2xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname,file\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_2xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":false,\\\"pcode\\\":12,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"*\",\"$update_option\":\"avg\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_5xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"account.log\",\"$include_filter_values\":\"status_5xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_5xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"}]",
                          "single": false
                      },
                      {
                          "id": 5,
                          "type": "event",
                          "name": "LOG_REALTIME",
                          "data": "[{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"SMS 알림 발생\",\"tag_select_rule\":\"caller=='EventContextManager.expired(72)'&&key2!='EndedOK'\",\"event_message\":\"호스트명 : ${oname}\\n에러내용 : SMS 알림이 발생했습니다.\\n로그내용 : ${logContent}\",\"category\":\"yard\",\"keyword\":\"/data/whatap/logs/yard.log\",\"enabled\":false},{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"키워드 알림 테스트\",\"tag_select_rule\":\"\",\"event_message\":\"${oname}\\n${content}\",\"category\":\"undertow_access_log\",\"keyword\":\"/data/whatap/logs/undertow_access_log.log\",\"enabled\":false}]",
                          "single": false
                      },
                      // 프로젝트 생성 시, 사용자에게 노출하는 메타 정보로, 아래에서 자세히 다룹니다.
                      {
                          "id": 8,
                          "type": "meta",
                          "name": null,
                          "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
                          "single": true
                      }
                  ]
                }
                ```
                
            - document.meta
                - 프로젝트 생성 시, 프로젝트 카드 및 생성 단계에 표시할 메타 정보를 포함합니다.
                
                ```json
                {
                   "desc":{ 
                      "icon":"kafka", // 카드에 표시할 아이콘으로, 프론트 asset에 미리 추가되어있어야합니다.
                      "pricingUrl":"https://www.whatap.io/ko/pricing/#server-space", // '가격 정책' 링크 url
                      "summary":{
                          //프로젝트 카드와 생성 단계의 제품 설명에 표시됩니다.
                         "ko":"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.",
                         "ja":"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。",
                         "en":"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights."
                      }
                   },
                   //사용자에게 노출시키고 싶은 서비스 도메인으로, 아래에 포함되는 도메인에서만 카드가 노출됩니다.
                   "releaseEnvs":[
                      "DEV",
                      "PREVIEW",
                      "SERVICE"
                   ]
                }
                ```
                

### 피처 상세 조회

- 기존에 생성되어있던 피처 정보를 확인하려면 상세 조회 api를 호출합니다.
    - Signature
        - **[GET] /admin/api/feature**
        - query-params
            - textKey (필수)
        - response
            - response body
                
                ```json
                // response body
                {
                    "msg": "success",
                    "code": 200,
                    "data": `${FeatureDetail Object}`,
                    "ok": true
                }
                
                ```
                
            - FeatureDetail Object
                
                ```json
                {
                  "id": 9,
                  "productType": "APM",
                	"platform": "GO",
                	"textKey": "KAFKA", // feature 식별을 위한 고유값(중복 불가)
                	"name": "INFRA-TEST",  // display name. UI 에서는 해당 값으로 표시됩니다.
                	"description": "FEATURE INFRA TEST", // UI에 표시되지 않는 메타 정보
                	"status": "beta", // "open" 인 경우에만 서비스에 노출됩니다.
                	"document": [
                    {
                        "id": 6,
                        "type": "event",
                        "name": "COMPOSITE_LOG",
                        "data": "[{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_2xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"AppLog\",\"$include_filter_values\":\"status_2xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname,file\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_2xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":false,\\\"pcode\\\":12,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"*\",\"$update_option\":\"avg\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_5xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"account.log\",\"$include_filter_values\":\"status_5xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_5xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"}]",
                        "single": false
                    },
                    {
                        "id": 5,
                        "type": "event",
                        "name": "LOG_REALTIME",
                        "data": "[{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"SMS 알림 발생\",\"tag_select_rule\":\"caller=='EventContextManager.expired(72)'&&key2!='EndedOK'\",\"event_message\":\"호스트명 : ${oname}\\n에러내용 : SMS 알림이 발생했습니다.\\n로그내용 : ${logContent}\",\"category\":\"yard\",\"keyword\":\"/data/whatap/logs/yard.log\",\"enabled\":false},{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"키워드 알림 테스트\",\"tag_select_rule\":\"\",\"event_message\":\"${oname}\\n${content}\",\"category\":\"undertow_access_log\",\"keyword\":\"/data/whatap/logs/undertow_access_log.log\",\"enabled\":false}]",
                        "single": false
                    },
                    
                		// 프로젝트 생성 시, 사용자에게 노출하는 메타 정보로, 아래에서 자세히 다룹니다.
                		{
                        "id": 8,
                        "type": "meta",
                        "name": null,
                        "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
                        "single": true
                     }
                	]
                }
                ```
                

## 피처 추가하기

[feature_create](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/Untitled.json)

- 아래 Signatue에 맞게 api를 호출합니다.
    - **[POST] /admin/api/feature/create**
    - body params
        - body param 구성 예시
            
            ```json
            {
                "productType": "SMS",
                "platform": "INFRA",
                "textKey": "NEW_KAFKA",
                "name": "NEW Kafka",
                "description": "새로운 카프카",
                "status": "open",
                "document": [
                  {
                    "type": "event",
                    "name": "COMPOSITE_METRICS",
                    "data": "[{\"interval_sec\":60,\"query\":\"CATEGORY telegraf_kafka_controller\\nTAGLOAD {backward:true}\\nSELECT [ 'pcode', 'time', 'oid', 'Value', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"Value\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"KafkaController\\\" }\\nFILTER { key: \\\"name\\\", value: \\\"OfflinePartitionsCount\\\" }\\nGROUP { timegroup:10s, pk:pcode, merge:[Value]}\\nUPDATE { key:[Value], value:sum, keep: \\\"time\\\" }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"Value\\\"]\\n\",\"rule\":\"Value > 0\",\"event_level\":30,\"event_title\":\"Offline Partitions Detected\",\"time_trim\":5000,\"event_message\":\"There are currently ${Value} offline partitions. Immediate investigation and resolution are required to maintain cluster integrity.\",\"enabled\":true,\"time_period\":30000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714379700000,\\\"etime\\\":1714380300000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"2febe921-21fc-4019-9d5e-d29d7b1443ba\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY telegraf_kafka_server\\nTAGLOAD {backward:true}\\nSELECT [ 'pcode', 'time', 'oid', 'Value', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"Value\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"ReplicaManager\\\" }\\nFILTER { key: \\\"name\\\", value: \\\"UnderReplicatedPartitions\\\" }\\nFIRST-ONLY { key: \\\"oid\\\" }\\nGROUP { timeunit:10s, pk:pcode, merge:[Value] }\\nUPDATE { key:[Value], value:sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"Value\\\"]\\n\",\"rule\":\"Value > 0\",\"event_level\":30,\"event_title\":\"Under-Replicated Partitions Found\",\"time_trim\":5000,\"event_message\":\"There are ${Value} under-replicated partitions in the cluster. This may risk data loss and reduced fault tolerance.\",\"enabled\":true,\"time_period\":60000,\"stateful\":true,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714380660000,\\\"etime\\\":1714381260000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"4ae8ca05-6e0e-4c6e-bafc-2beb858f5448\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY telegraf_kafka_controller\\nTAGLOAD {backward:true}\\nSELECT [ 'pcode','oid', 'time', 'oid', 'Value', 'type', 'name' ]\\nFILTER { key: \\\"Value\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"KafkaController\\\" }\\nFILTER { key: \\\"name\\\", value: \\\"ActiveControllerCount\\\" }\\nGROUP { timegroup:\\\"10s\\\", pk:\\\"pcode\\\", merge:[Value], keep:\\\"time\\\" }\\nUPDATE { key:[Value], value:sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"Value\\\"]\\n\",\"rule\":\"Value != 1\",\"event_level\":30,\"event_title\":\"Controller Count Issue Detected\",\"time_trim\":5000,\"event_message\":\"The number of active controllers is ${Value}. There should be exactly one active controller in the cluster.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714391460000,\\\"etime\\\":1714392060000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"54b28e6a-eb81-4224-b0c4-a7362fdc9b03\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY telegraf_kafka_controller\\nTAGLOAD {backward:true}\\nSELECT [ 'pcode', 'time', 'oid', 'OneMinuteRate', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"OneMinuteRate\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"ControllerStats\\\" }\\nFILTER { key: \\\"name\\\", value: \\\"UncleanLeaderElectionsPerSec\\\" }\\nFIRST-ONLY { key: \\\"oid\\\" }\\nGROUP { timeunit:10s, pk:pcode, merge:[OneMinuteRate] }\\nUPDATE { key:[OneMinuteRate], value:sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"Value\\\"]\\n\",\"rule\":\"Value > 0\",\"event_level\":30,\"event_title\":\"Unclean Leader Elections Occurring\",\"time_trim\":5000,\"event_message\":\" There have been ${Value} unclean leader elections. This can lead to potential data loss.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714391940000,\\\"etime\\\":1714392540000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"c35b6180-d34d-4912-b831-fad323b7f83e\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY {\\\"telegraf_kafka_server\\\":6h, \\\"telegraf_kafka_server{m5}\\\":3d, \\\"telegraf_kafka_server{h1}\\\":unlimit } \\nTAGLOAD\\nSELECT [ 'pcode', 'time', 'oid', 'OneMinuteRate', 'pname', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"OneMinuteRate\\\", exist: true }\\nFILTER { key: \\\"pname\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"ReplicaManager\\\"}\\nFILTER { key: \\\"name\\\", value: \\\"IsrShrinksPerSec\\\"}\\nGROUP { timegroup:\\\"10s\\\", merge: ['OneMinuteRate'], pk: \\\"pcode\\\", last: time}\\nUPDATE { key: ['OneMinuteRate'], value: sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"OneMinuteRate\\\"]\\n\",\"rule\":\"FifteenMinuteRate*10 < OneMinuteRate\",\"event_level\":30,\"event_title\":\"High ISR Expansion Rate\",\"time_trim\":5000,\"event_message\":\"The ISR expansion rate has increased unexpectedly to ${OneMinuteRate} per minute. Monitor for potential stability issues.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714392060000,\\\"etime\\\":1714392660000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"2f0ff006-ced5-448d-88bf-a0debcb3ae89\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"OIDSET { oid:$oid, okind:$okind, onode:$onode }\\nCATEGORY {\\\"telegraf_kafka_server\\\":6h, \\\"telegraf_kafka_server{m5}\\\":3d, \\\"telegraf_kafka_server{h1}\\\":unlimit } \\nTAGLOAD\\nSELECT [ 'pcode', 'time', 'oid', 'OneMinuteRate', 'pname', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"OneMinuteRate\\\", exist: true }\\nFILTER { key: \\\"pname\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"ReplicaManager\\\"}\\nFILTER { key: \\\"name\\\", value: \\\"IsrShrinksPerSec\\\"}\\nGROUP { timeunit: 10s, merge: ['OneMinuteRate'], pk:pcode, last: time}\\nUPDATE { key: \\\"OneMinuteRate\\\", value: sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"OneMinuteRate\\\"]\\n\",\"rule\":\"FifteenMinuteRate * 10 < OneMinuteRate\",\"event_level\":30,\"event_title\":\"Increased ISR Shrink Rate\",\"time_trim\":5000,\"event_message\":\"The ISR shrink rate is currently ${OneMinuteRate} per minute. This could indicate synchronization problems among replicas.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714392660000,\\\"etime\\\":1714393260000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"6d797975-86a6-4ab8-ab93-ce8ba0d04ed6\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY {\\\"telegraf_kafka_server\\\":6h, \\\"telegraf_kafka_server{m5}\\\":3d, \\\"telegraf_kafka_server{h1}\\\":unlimit } \\nTAGLOAD\\nSELECT [ 'pcode', 'time', 'oid', 'OneMinuteRate', 'oname', 'type', 'name' ]\\nSKIP 3\\nFILTER { key: \\\"OneMinuteRate\\\", exist: true }\\nFILTER { key: \\\"oname\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"SessionExpireListener\\\"}\\nFILTER { key: \\\"name\\\", value: \\\"ZooKeeperExpiresPerSec\\\"}\\nGROUP { timeunit: 10s, merge: ['OneMinuteRate'], pk: pcode, last: time }\\nUPDATE { key: ['OneMinuteRate'], value: sum }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"OneMinuteRate\\\"]\\n\",\"rule\":\"FifteenMinuteRate*10 < OneMinuteRate\",\"event_level\":30,\"event_title\":\"Zookeeper Connection Issues\",\"time_trim\":5000,\"event_message\":\"Issues with Zookeeper synchronization have been detected. This may affect cluster stability and performance.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714393020000,\\\"etime\\\":1714393620000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"2165e90e-9e8b-49ee-969d-13b76585d625\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"},{\"interval_sec\":60,\"query\":\"CATEGORY telegraf_kafka_server\\nTAGLOAD {backward:true}\\nSELECT [ 'pcode', 'oid', 'time', 'oid', 'Value', 'type', 'name' ]\\nFILTER { key: \\\"Value\\\", exist: true }\\nFILTER { key: \\\"type\\\", value: \\\"ReplicaManager\\\" }\\nFILTER { key: \\\"name\\\", value: \\\"LeaderCount\\\" }\\nGROUP {timegroup:\\\"10s\\\", pk:\\\"pcode\\\", merge:[Value], keep:\\\"time\\\" }\\nUPDATE { key:[Value], value:count }\\nSKIP 1\\nLIMIT 1\\nSELECT [\\\"time\\\",\\\"Value\\\"]\\n\",\"rule\":\"Value < 3\",\"event_level\":30,\"event_title\":\"Broker Count Below Threshold\",\"time_trim\":5000,\"event_message\":\"The current broker count is ${Value}. This is below the required threshold for normal operations and may affect cluster performance.\",\"enabled\":true,\"time_period\":60000,\"stateful\":false,\"silent_sec\":300,\"desc\":\"{\\\"widgetType\\\":\\\"EXPERT\\\",\\\"supports\\\":[],\\\"isExpertEditable\\\":false,\\\"flexEventWidget\\\":{\\\"widgetType\\\":\\\"FLEX_EVENT\\\",\\\"id\\\":\\\"composite_metrics_widget\\\",\\\"requestApi\\\":\\\"LAST\\\",\\\"option\\\":{\\\"stime\\\":1714393200000,\\\"etime\\\":1714393800000,\\\"liveUpdateIntervalSec\\\":0,\\\"globalTime\\\":false,\\\"chart\\\":\\\"SERIES\\\",\\\"pcodes\\\":[2529],\\\"flex_event\\\":{\\\"category\\\":\\\"server_base\\\",\\\"tagPksGroup\\\":{\\\"pks\\\":[\\\"oid\\\"],\\\"timeunit\\\":5000},\\\"fieldsWithMerges\\\":[{\\\"key\\\":\\\"cpu\\\",\\\"timeMerge\\\":\\\"AVG\\\",\\\"objectMerge\\\":\\\"AVG\\\",\\\"unit\\\":\\\"PERCENT\\\",\\\"_label\\\":\\\"8ba23d92-b4e0-4836-abe6-51cf31944655\\\"}]},\\\"chartAside\\\":{\\\"chart\\\":\\\"TABLE\\\"},\\\"timeAction\\\":\\\"CUSTOM\\\"},\\\"metrics\\\":[{\\\"mql\\\":\\\"INJECT timepast\\\\nHEADER { \\\\\\\"cpu$\\\\\\\":\\\\\\\"PERCENT\\\\\\\" }\\\\nOIDSET { oid:$oid, okind:$okind, onode:$onode }\\\\nCATEGORY \\\\\\\"server_base\\\\\\\"\\\\nTAGLOAD\\\\nINJECT default\\\\nUPDATE {key: cpu, value: avg}\\\\nGROUP {pk:[oid], timeunit: 5000}\\\\nUPDATE {key: cpu, value: avg}\\\\nCREATE {key: _id_, expr:\\\\\\\"oid\\\\\\\"}\\\\nCREATE {key: _name_, expr:\\\\\\\"oid\\\\\\\"} \\\\nSELECT [_name_, _id_, time, oid, cpu]\\\\n\\\"}]},\\\"pcode\\\":2529}\"}]",
                    "single": false
                  },
                  {
                    "type": "event",
                    "name": "BASIC",
                    "data": "[\"kafka001\",\"kafka002\",\"kafka003\",\"kafka004\",\"kafka005\",\"kafka006\",\"kafka007\",\"kafka008\",\"kafka009\"]",
                    "single": false
                  },
                  {
                    "type": "event",
                    "name": "ANOMALY",
                    "data": "[{\"eventMessage\":\"[이상치탐지] 네트워크 Packet Out ${packetOut}\",\"objectMerge\":null,\"ignoreNegative\":false,\"ignorePositive\":false,\"receiver\":[],\"pcode\":12,\"silentSec\":10800000,\"negativeScore\":12,\"enabled\":false,\"tags\":{\"oname\":\"*\"},\"filter\":null,\"positiveScore\":12,\"eventLevelText\":\"Warning\",\"width\":0.99,\"id\":\"2a21593544e141ee8a992bb889e54c27\",\"category\":\"server_network{m5}\",\"fields\":[\"packetOut\"],\"repeatCount\":2},{\"eventMessage\":\"rttet\",\"objectMerge\":null,\"ignoreNegative\":false,\"ignorePositive\":false,\"receiver\":[],\"pcode\":12,\"silentSec\":10800000,\"negativeScore\":8,\"enabled\":false,\"tags\":{\"oname\":\"Dev-Modules\"},\"filter\":null,\"positiveScore\":8,\"eventLevelText\":\"Warning\",\"width\":0.99,\"id\":\"48f9217fbb4148dbb81b4f23cb51cec7\",\"category\":\"server_base{m5}\",\"fields\":[\"cpu\"],\"repeatCount\":2}]",
                    "single": false
                  },
                  {
                    "type": "event",
                    "name": "METRICS",
                    "data": "[{\"eventMessage\":\"harim tag test\",\"eventTitle\":\"harim test1\",\"repeatDuration\":0,\"select\":\"oname == 'dev-front'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 3\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"TEST || ${projectName} ${oname} - CPU used ${cpu}\",\"eventTitle\":\"TEST 123\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":10,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 5\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0},{\"eventMessage\":\"TEST || ${projectName} ${oname} - CPU used ${cpu}\",\"eventTitle\":\"TEST 123\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":10,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 5\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0},{\"eventMessage\":\"지니오 테스트당~~~\",\"eventTitle\":\"지니오 테스트\",\"repeatDuration\":10000,\"select\":\"\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 30\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":1},{\"eventMessage\":\"test, Epochtime: ${epochtime}, memory_pused: ${memory_pused}, $pname, ${projectName}\",\"eventTitle\":\"harim test2\",\"repeatDuration\":0,\"select\":\"oname == 'dev-agency'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 0.9\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"Memory > 90%\",\"eventTitle\":\"hsnam memory test\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"memory_pused > 90\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"Infobip 으로 보냈습니다.\",\"eventTitle\":\"harim SMS test\",\"repeatDuration\":0,\"select\":\"oname == 'dev-front'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 2\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"${oname} ${mountPoint} has ${freePercent}% left in space. please clean up the server.\",\"eventTitle\":\"Low Disk_Clean Up Needed\",\"repeatDuration\":0,\"select\":\"mountPoint != 'value'\",\"eventLevel\":30,\"alertLabel\":[\"mountPoint\",\"oid\"],\"rule\":\"freePercent <= 15\",\"silentSec\":300,\"category\":\"server_disk\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0}]",
                    "single": false
                  },
                  {
                    "type": "event",
                    "name": "LOG_REALTIME",
                    "data": "[{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"SMS 알림 발생\",\"tag_select_rule\":\"caller=='EventContextManager.expired(72)'&&key2!='EndedOK'\",\"event_message\":\"호스트명 : ${oname}\\n에러내용 : SMS 알림이 발생했습니다.\\n로그내용 : ${logContent}\",\"category\":\"yard\",\"keyword\":\"/data/whatap/logs/yard.log\",\"enabled\":false},{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"키워드 알림 테스트\",\"tag_select_rule\":\"\",\"event_message\":\"${oname}\\n${content}\",\"category\":\"undertow_access_log\",\"keyword\":\"/data/whatap/logs/undertow_access_log.log\",\"enabled\":false}]",
                    "single": false
                  },
                  {
                    "type": "event",
                    "name": "COMPOSITE_LOG",
                    "data": "[{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_2xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"AppLog\",\"$include_filter_values\":\"status_2xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname,file\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_2xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":false,\\\"pcode\\\":12,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"*\",\"$update_option\":\"avg\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_5xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"account.log\",\"$include_filter_values\":\"status_5xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_5xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"}]",
                    "single": false
                  },
                  {
                    "type": "installation",
                    "data": "{\"ja\":{\"title\":\"設置前の注意事項\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntuサポートバージョン\",\"version\":\"12.04以上\"},{\"type\":\"support-version\",\"title\":\"Kafka サポートバージョン\",\"version\":\"Apache Kafka 3.x以降\"},{\"type\":\"support-version\",\"title\":\"OS対応バージョン\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"オペレーティングシステムのアーキテクチャ\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"アクセスキーの確認\",\"description\":\"アクセスキーは、ワタップサービスを有効にするための一意のIDです。\\n{get_license_feature}\"},{\"title\":\"インストールスクリプトの生成\",\"boxes\":[{\"prepend\":\"KAFKAがインストールされているサーバーにスクリプトを生成するには、以下のコマンドを実行してください。\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"以下のコマンドを実行してください。\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"モニタリングを始める\",\"description\":\"KAFKAでJolokiaエージェントを設定するには、以下のコマンドを実行して再起動してください。\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]},\"en\":{\"title\":\"Precautions before installation\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntu supported versions\",\"version\":\"12.04 or higher\"},{\"type\":\"support-version\",\"title\":\"Kafka supported versions\",\"version\":\"Apache Kafka 3.x or higher\"},{\"type\":\"support-version\",\"title\":\"OS supported version\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"Operating system architecture\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"Check access key\",\"description\":\"The access key is a unique ID for activating the WhaTap service.\\n{get_license_feature}\"},{\"title\":\"Generate installation script\",\"boxes\":[{\"prepend\":\"Run the command below to create a script on the server where KAFKA is installed.\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"Run the command below.\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"Start monitoring\",\"description\":\"To set up the Jolokia agent in KAFKA, run the command below and then restart.\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]},\"ko\":{\"title\":\"설치 전 유의사항\",\"icon\":\"kafka\",\"supports\":[{\"type\":\"support-version\",\"title\":\"Ubuntu 지원 버전\",\"version\":\"12.04 이상\"},{\"type\":\"support-version\",\"title\":\"Kafka 지원 버전\",\"version\":\"Apache Kafka 3.x 이상\"},{\"type\":\"support-version\",\"title\":\"OS 지원 버전\",\"version\":\"Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)\"},{\"type\":\"support-version\",\"title\":\"운영체제 아키텍처\",\"version\":\"Amd64/X86_64, Arm64/Aarch64 \"},{\"type\":\"whatap-proxy\"}],\"step\":[{\"title\":\"액세스 키 확인\",\"description\":\"액세스 키는 와탭 서비스 활성화를 위한 고유 ID입니다.\\n{get_license_feature}\"},{\"title\":\"설치 스크립트 생성\",\"boxes\":[{\"prepend\":\"KAFKA가 설치된 서버에 스크립트를 생성하기 위해 아래 명령어를 실행하세요.\",\"data\":\"curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\\n-o install_kafka_monitoring.sh\",\"option\":\"copy\"},{\"prepend\":\"아래 명령어를 실행하세요.\",\"data\":\"chmod +x install_kafka_monitoring.sh\\n./install_kafka_monitoring.sh \\\"{license_key}\\\" \\\"{proxy_server}\\\"\",\"option\":\"copy\"}]},{\"title\":\"모니터링 시작하기\",\"description\":\"KAFKA에 Jolokia 에이전트 설정을 위해 아래 명령어를 실행 후 재시작하세요.\",\"boxes\":[{\"data\":\"#cd {kafka home directory}/bin\\r\\nsed -i '/^#!/a export KAFKA_OPTS='\\\\''-javaagent:/usr/whatap/infra/feature/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\\\''' kafka-server-start.sh\\r\\n./kafka-server-stop.sh\\r\\n./kafka-server-start.sh\",\"option\":\"copy\"}]}]}}",
                    "single": true
                  },
                  {
                    "type": "meta",
                    "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
                    "single": true
                  }
                ]
              }
            ```
            
        
        ```json
        // platform, textKey PK
        // status는 alpha, beta, open, closed 중 한가지값
        {
            "platform":"GO",
            "textKey":"KAFKA",
            "name":"INFRA-TEST",
            "description":"FEATURE INFRA TEST",
            "status":"beta",
            //document 를 구성하는 value 들은 모두 JSON을 string 으로 변환한 값이 포함됩니다. 
            //변환 방법과 예시는 아래에서 자세히 다룹니다.
            "document": [
        	    "meta": "...",
        	    "installation":"...",
        	    "event":"...",
        	    "dashboard": "..."
            ],
        }
        ```
        
        - document > meta
            - 프로젝트 생성 시, 프로젝트 카드 및 생성 단계에 표시할 메타 정보를 포함합니다.
            - [구성 정보](https://www.notion.so/Feature-34a75e94062f4f4786ee06022291da33?pvs=21)를 아래와 같은 형태로 정의합니다.
                
                ```json
                {
                  "type": "meta", 
                  // 구성 정보를 JSON.stringify 처리하여 전달합니다.
                  "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
                  "single": true // meta는 피처 당 1개만 존재해야하므로, 해당 값을 반드시 true로 전달합니다.
                }
                ```
                
    
    <aside>
    💡 온라인 툴로 JSON을 stringify 하는 방법도 있으나, 이 경우 불필요한 공백이 포함된 결과가 반환됩니다. 
    대략 10개 정도의 온라인툴로 테스트 해봤는데, 불필요한 공백을 제외해주는 걸 찾지 못했습니다. 
    때문에 불편하지만 확실한 방법을 위쪽에 별도로 설명하오니, 참고 부탁드립니다.
    [stringify 처리로 이동](https://www.notion.so/Feature-34a75e94062f4f4786ee06022291da33?pvs=21)
    
    </aside>
    
     
    
    - document > installation
        - 에이전트 설치 페이지에 표시할 구성 정보를 포함합니다.
        - 구성 정보는 아래와 같습니다.
            - server-kafka 피처의 installation  구성 예시
                
                ```json
                {
                  "ko": {
                	  "title": "設置前の注意事項",
                    "icon": "kafka",
                    "supports": [
                      {
                        "type": "support-version",
                        "title": "Ubuntuサポートバージョン",
                        "version": "12.04以上"
                      },
                      {
                        "type": "support-version",
                        "title": "Kafka サポートバージョン",
                        "version": "Apache Kafka 3.x以降"
                      },
                      {
                        "type": "support-version",
                        "title": "OS対応バージョン",
                        "version": "Redhat6 or equivalent(CentOS, Rocky Linux, Amazon Linux)"
                      },
                      {
                        "type": "support-version",
                        "title": "オペレーティングシステムのアーキテクチャ",
                        "version": "Amd64/X86_64, Arm64/Aarch64 "
                      },
                      {
                        "type": "whatap-proxy"
                      }
                    ],
                    "step": [
                      {
                        "title": "アクセスキーの確認",
                        "description": "アクセスキーは、ワタップサービスを有効にするための一意のIDです。\n{get_license_feature}"
                      },
                      {
                        "title": "インストールスクリプトの生成",
                        "boxes": [
                          {
                            "prepend": "KAFKAがインストールされているサーバーにスクリプトを生成するには、以下のコマンドを実行してください。",
                            "data": "curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\n-o install_kafka_monitoring.sh",
                            "option": "copy"
                          },
                          {
                            "prepend": "以下のコマンドを実行してください。",
                            "data": "chmod +x install_kafka_monitoring.sh\n./install_kafka_monitoring.sh \"{license_key}\" \"{proxy_server}\"",
                            "option": "copy"
                          }
                        ]
                      },
                      {
                        "title": "モニタリングを始める",
                        "description": "KAFKAでJolokiaエージェントを設定するには、以下のコマンドを実行して再起動してください。",
                        "boxes": [
                          {
                            "data": "#cd {kafka home directory}\/bin\r\nsed -i '\/^#!\/a export KAFKA_OPTS='\\''-javaagent:\/usr\/whatap\/infra\/feature\/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\''' kafka-server-start.sh\r\n.\/kafka-server-stop.sh\r\n.\/kafka-server-start.sh",
                            "option": "copy"
                          }
                        ]
                      }
                    ]
                  },
                  
                  
                  "en": {...},
                  "ja": {...}
                }
                ```
                
            
            ```json
            {
              //각 언어 별로 들어갈 컨텐츠를 정의해야합니다.
              "ko": {
            	  "title": "설치 페이지 제목",
                "icon": "kafka", // icon 은 사전에 프론트 asset에 포함되어 있어야 합니다.
                //지원 버전과 Whatap proxy 주소를 표시합니다.
                "supports": [
                  // 지원 버전을 표시할 경우 아래 형식의 Object 를 추가하세요. (복수)
                  {
                    "type": "support-version", 
                    "title": "Ubuntu 지원 버전", // 지원 버전에 대한 label
                    "version": "12.04이상"  // 표기할 버전
                  },
                  {
                    "type": "support-version",
                    "title": "Cenos 지원 버전",
                    "version": "6.4이상"
                  },
                  {
                    "type": "whatap-proxy" // 타입만 적어줍니다. 주소와 port는 서버 환경에 맞게 자동으로 표시합니다.
                  }
                ],
                // 설치 단계를 표시할 내용입니다.
                "step": [
                  // 표시할 단계의 수만큼 Object 를 추가합니다. (복수)
                  {
                    "title": "액세스 키 확인",
                    "description": "액세스 키는 와탭 서비스 활성화를 위한 고유 ID입니다.\n{get_license_feature}"
                  },
                  {
                    "title": "설치 스크립트 생성",
                    //스크립트 구문을 표시하고자 할 경우, boxes 속성을 아래와 같이 정의하세요.
                    "boxes": [
                      {
                        "prepend": "KAFKA가 설치된 서버에 스크립트를 생성하기 위해 아래 명령어를 실행하세요.",
                        //코드 블록에 표시될 내용
                        "data": "curl http://repo.whatap.io/telegraf/feature/kafka/install_kafka_monitoring.sh\n-o install_kafka_monitoring.sh",
            						//option field를 명시하지 않을 경우, copy를 할 수 없습니다.
                        "option": "copy" 
                      },
                      {
                        "prepend": "아래 명령어를 실행하세요.",
                        "data": "chmod +x install_kafka_monitoring.sh\n./install_kafka_monitoring.sh \"{license_key}\" \"{proxy_server}\"",
                        "option": "copy"
                      }
                    ]
                  },
                  {
                    "title": "모니터링 시작하기",
                    "description": "KAFKA에 Jolokia 에이전트 설정을 위해 아래 명령어를 실행 후 재시작하세요.",
                    "boxes": [
                      {
                        "data": "#cd {kafka home directory}\/bin\r\nsed -i '\/^#!\/a export KAFKA_OPTS='\\''-javaagent:\/usr\/whatap\/infra\/feature\/jolokia-jvm-agent.jar=port=8778,host=127.0.0.1'\\''' kafka-server-start.sh\r\n.\/kafka-server-stop.sh\r\n.\/kafka-server-start.sh",
                        "option": "copy"
                      }
                    ]
                  }
                ]
              },
              "en": {...},
              "ja": {...}
            }
            ```
            
        
        - 구성 정보를 아래 형태로 정의합니다.
        
        ```json
        {
          "type": "installation", 
          // 구성 정보를 JSON.stringify 처리하여 전달합니다.
          "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
          "single": true // installation 은 피처 당 1개만 존재해야하므로, 해당 값을 반드시 true로 전달합니다.
        }
        ```
        
    
    <aside>
    💡 위 예시에 나열된 기능 이외에 추가적인 요구사항이 있으실 경우, @준영 최 문의 부탁드립니다.
    
    </aside>
    
    - document > event
        - 피처의 이벤트에 해당하는 메타 정보로, 다음 상황에 활용됩니다.
            - 프로젝트 생성 → 라이센스 발급 시 **기본으로 추가되는 이벤트**
            - 이벤트 V2 → 이벤트 추가 → 생성 가능한 **이벤트 템플릿 목록** 표시
        - 이벤트는 종류에 맞는 데이터를 전달해야합니다.
            - 기본 이벤트의 data
                
                ```json
                // 서버에 저장된 템플릿의 id 목록을 전달합니다.
                [
                	"kafka001",
                	"kafka002",
                	"kafka003",
                	"kafka004",
                	...
                ]
                ```
                
            
             아래 나머지 이벤트의 경우, v1 에서 사용하던 각각의 json 형식을 그대로 사용합니다.
            
            - 메트릭스
            - 복합 메트릭스
            - 이상치 탐지
            - 실시간 로그
            - 복합 로그
            - ~~히트맵 (추후)~~
            
            ex) 복합 메트릭스
            
            ```json
            //메트릭스 이벤트의 json 양식을 그대로 사용합니다.
            [
              {
                "eventMessage": "harim tag test",
                "eventTitle": "harim test1",
                "repeatDuration": 0,
                "select": "oname == 'dev-front'",
                "eventLevel": 30,
                "alertLabel": [
                  "oid"
                ],
                "rule": "cpu > 3",
                "silentSec": 0,
                "category": "server_base",
                "enabled": false,
                "stateful": true,
                "repeatCount": 0
              }
            ]
            ```
            
        
        - 데이터를 아래와 같은 형식으로 정의합니다.
        
        ```json
        {
          "type": "event",
          //- 기본이벤트: "Basic"
          //- 메트릭스: "METRICS"
        	//- 복합 메트릭스: "COMPOSITE_METRICS"
        	//- 이상치 탐지: "ANOMALY"
        	//- 실시간 로그: "REALTIME_LOG"
        	//- 복합 로그: "COMPOSITE_LOG"
          "name": "BASIC", 
          // stringify 하여 전달합니다.
          "data": "[\"kafka001\",\"kafka002\",\"kafka003\",\"kafka004\",\"kafka005\",\"kafka006\",\"kafka007\",\"kafka008\",\"kafka009\"]",
          "single": false // 이벤트는 복수개를 정의할 수 있으므로, 반드시 false 로 전달해야합니다.
        },
        ```
        
    - document > dashboard

## 피처 업데이트

[feature_update.json](Feature%20%E1%84%80%E1%85%AA%E1%86%AB%E1%84%85%E1%85%B5%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%2034a75e94062f4f4786ee06022291da33/feature_update.json)

- [POST] /admin/api/feature/update
- body
    
    ```json
    {
      "productType": "SMS",
      "platform": "INFRA",
      "textKey": "NEW_KAFKA",
      "name": "NEW Kafka",
      "description": "새로운 카프카",
      "status": "open",
      "document": [
        {
          "id": 53,
          "type": "event",
          "name": "BASIC",
          "data": "[\"kafka001\",\"kafka002\",\"kafka003\",\"kafka004\",\"kafka005\",\"kafka006\",\"kafka007\",\"kafka008\",\"kafka009\"]",
          "single": false
        },
        {
          "id": 54,
          "type": "event",
          "name": "ANOMALY",
          "data": "[{\"eventMessage\":\"[이상치탐지] 네트워크 Packet Out ${packetOut}\",\"objectMerge\":null,\"ignoreNegative\":false,\"ignorePositive\":false,\"receiver\":[],\"pcode\":12,\"silentSec\":10800000,\"negativeScore\":12,\"enabled\":false,\"tags\":{\"oname\":\"*\"},\"filter\":null,\"positiveScore\":12,\"eventLevelText\":\"Warning\",\"width\":0.99,\"id\":\"2a21593544e141ee8a992bb889e54c27\",\"category\":\"server_network{m5}\",\"fields\":[\"packetOut\"],\"repeatCount\":2},{\"eventMessage\":\"rttet\",\"objectMerge\":null,\"ignoreNegative\":false,\"ignorePositive\":false,\"receiver\":[],\"pcode\":12,\"silentSec\":10800000,\"negativeScore\":8,\"enabled\":false,\"tags\":{\"oname\":\"Dev-Modules\"},\"filter\":null,\"positiveScore\":8,\"eventLevelText\":\"Warning\",\"width\":0.99,\"id\":\"48f9217fbb4148dbb81b4f23cb51cec7\",\"category\":\"server_base{m5}\",\"fields\":[\"cpu\"],\"repeatCount\":2}]",
          "single": false
        },
        {
          "id": 55,
          "type": "event",
          "name": "METRICS",
          "data": "[{\"eventMessage\":\"harim tag test\",\"eventTitle\":\"harim test1\",\"repeatDuration\":0,\"select\":\"oname == 'dev-front'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 3\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"TEST || ${projectName} ${oname} - CPU used ${cpu}\",\"eventTitle\":\"TEST 123\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":10,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 5\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0},{\"eventMessage\":\"TEST || ${projectName} ${oname} - CPU used ${cpu}\",\"eventTitle\":\"TEST 123\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":10,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 5\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0},{\"eventMessage\":\"지니오 테스트당~~~\",\"eventTitle\":\"지니오 테스트\",\"repeatDuration\":10000,\"select\":\"\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 30\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":1},{\"eventMessage\":\"test, Epochtime: ${epochtime}, memory_pused: ${memory_pused}, $pname, ${projectName}\",\"eventTitle\":\"harim test2\",\"repeatDuration\":0,\"select\":\"oname == 'dev-agency'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 0.9\",\"silentSec\":300,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"Memory > 90%\",\"eventTitle\":\"hsnam memory test\",\"repeatDuration\":0,\"select\":\"\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"memory_pused > 90\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"Infobip 으로 보냈습니다.\",\"eventTitle\":\"harim SMS test\",\"repeatDuration\":0,\"select\":\"oname == 'dev-front'\",\"eventLevel\":30,\"alertLabel\":[\"oid\"],\"rule\":\"cpu > 2\",\"silentSec\":0,\"category\":\"server_base\",\"enabled\":false,\"stateful\":true,\"repeatCount\":0},{\"eventMessage\":\"${oname} ${mountPoint} has ${freePercent}% left in space. please clean up the server.\",\"eventTitle\":\"Low Disk_Clean Up Needed\",\"repeatDuration\":0,\"select\":\"mountPoint != 'value'\",\"eventLevel\":30,\"alertLabel\":[\"mountPoint\",\"oid\"],\"rule\":\"freePercent <= 15\",\"silentSec\":300,\"category\":\"server_disk\",\"enabled\":false,\"stateful\":false,\"repeatCount\":0}]",
          "single": false
        },
        {
          "id": 56,
          "type": "event",
          "name": "LOG_REALTIME",
          "data": "[{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"SMS 알림 발생\",\"tag_select_rule\":\"caller=='EventContextManager.expired(72)'&&key2!='EndedOK'\",\"event_message\":\"호스트명 : ${oname}\\n에러내용 : SMS 알림이 발생했습니다.\\n로그내용 : ${logContent}\",\"category\":\"yard\",\"keyword\":\"/data/whatap/logs/yard.log\",\"enabled\":false},{\"skiptime\":1000,\"field\":\"file\",\"event_level\":20,\"event_title\":\"키워드 알림 테스트\",\"tag_select_rule\":\"\",\"event_message\":\"${oname}\\n${content}\",\"category\":\"undertow_access_log\",\"keyword\":\"/data/whatap/logs/undertow_access_log.log\",\"enabled\":false}]",
          "single": false
        },
        {
          "id": 57,
          "type": "event",
          "name": "COMPOSITE_LOG",
          "data": "[{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_2xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"AppLog\",\"$include_filter_values\":\"status_2xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname,file\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_2xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":false,\\\"pcode\\\":12,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":0,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"*\",\"$update_option\":\"avg\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_count_v2\",\"rule\":\"include_count > 10\",\"event_title\":\"status_5xx_count\",\"enabled\":false,\"silent_sec\":300,\"query_param\":{\"$category\":\"account.log\",\"$include_filter_values\":\"status_5xx\",\"$denominator_filter_values\":\"\",\"$include_filter_keys\":\"status_nxx\",\"$aggr_keys\":\"\",\"$group_time_unit\":\"1d\",\"$exclude_filter_keys\":\"none\",\"$group_keys\":\"oname\",\"$exclude_filter_values\":\"none\",\"$denominator_filter_keys\":\"\"},\"event_level\":20,\"event_message\":\"${pname} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"templateType\\\":\\\"status_5xx_count\\\",\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[{\\\"aggregation\\\":\\\"count\\\",\\\"field\\\":\\\"include_count\\\",\\\"operation\\\":\\\">\\\",\\\"value\\\":10}],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_EVENT_INPUT_RULE\\\"}\"},{\"query_inject\":{},\"interval_sec\":60,\"query\":\"/v2/logs/logsink_rps\",\"rule\":\"rps > 10\",\"event_title\":\"Log RPS Event\",\"enabled\":false,\"silent_sec\":60,\"query_param\":{\"$category\":\"account.log\",\"$update_option\":\"sum\",\"$group_keys\":\"\"},\"event_level\":20,\"event_message\":\"${category} ${metricValue} ${metricOperator} ${metricThreshold}\",\"time_period\":60000,\"stateful\":true,\"desc\":\"{\\\"supports\\\":[{\\\"productType\\\":\\\"APM\\\"},{\\\"productType\\\":\\\"SMS\\\"},{\\\"productType\\\":\\\"CPM\\\"}],\\\"ruleInput\\\":[],\\\"isExpertEditable\\\":true,\\\"widgetType\\\":\\\"LOG_RPS_EVENT\\\"}\"}]",
          "single": false
        },
        {
          "id": 59,
          "type": "meta",
          "data": "{\"desc\":{\"icon\":\"kafka\",\"pricingUrl\":\"https://www.whatap.io/ko/pricing/#server-space\",\"summary\":{\"ko\":\"데이터 스트림의 이상 현상을 쉽게 추적하고 찾을 수 있는 Kafka 모니터링을 이용해 보세요. Kafka 서비스의 다양한 지표를 모니터링하고, 알림을 설정해 급증하는 트래픽을 미리 파악할 수 있습니다. 맞춤형 대시보드를 생성하고 모니터링해 포괄적인 통찰력을 확보하세요.\",\"ja\":\"データストリーミング上の異常をトレースし、容易に確認できるKafkaモニタリングが利用できます。Kafkaサービスの各種指標を監視し、アラートを設定することで、急増するトラフィックが事前に把握できます。業務に沿ったダッシュボードを生成して、使うことも可能です。\",\"en\":\"Kafka monitoring makes it easy to track and find anomalies in data streams. You can monitor various metrics of Kafka service, and set up alerts to catch spikes in traffic ahead of time. Create and monitor customized dashboards to gain comprehensive insights.\"}},\"releaseEnvs\":[\"DEV\",\"PREVIEW\",\"SERVICE\"]}",
          "single": true
        }
      ]
    }
    ```
    
    - textKey 로 feature 하나를 찾아냄 (unique)
    - name, description, status, document 값에 대해 update 수행
        - productType, platform, textKey 에 대해서는 update 할 수 없다.
    - document [] 내의 각 id 값으로 document 를 update 한다.
        - id 값을 지정해서 넘기는 경우 update, id를 넘기지 않는 경우 add 동작을 수행한다.
        - 해당 feature 에 지정한 id 값을 갖는 document 가 없을 경우 error
        (리스트 중 하나라도 잘못된 id 값이 포함된 경우 업데이트를 수행하지 않고 error 리턴)
    - 그 외의 내용은 [피처 추가하기](https://www.notion.so/Feature-34a75e94062f4f4786ee06022291da33?pvs=21)에서 설명된 내용과 같다.
- response
    
    ```json
    {
        "msg": "success",
        "code": 200,
        "data": {
            "id": 1,
            "productType": "SMS",
            "platform": "INFRA",
            "textKey": "NEW_KAFKA",
            "name": "Updated Kafka",
            "description": "업데이트된 카프카",
            "status": "open",
            "document": [
                {
                    "id": 3,
                    "type": "event",
                    "name": "ANOMALY",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 2,
                    "type": "event",
                    "name": "BASIC",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 6,
                    "type": "event",
                    "name": "COMPOSITE_LOG",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 1,
                    "type": "event",
                    "name": "COMPOSITE_METRICS",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 5,
                    "type": "event",
                    "name": "LOG_REALTIME",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 4,
                    "type": "event",
                    "name": "METRICS",
                    "data": "...",
                    "single": false
                },
                {
                    "id": 7,
                    "type": "installation",
                    "name": null,
                    "data": "...",
                    "single": true
                },
                {
                    "id": 8,
                    "type": "meta",
                    "name": null,
                    "data": "...",
                    "single": true
                }
            ]
        },
        "ok": true
    }
    ```