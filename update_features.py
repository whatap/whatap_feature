import json

def getDefaultFunc():

    return """
import json
mainJSON = json.loads(main.decode('utf-8'))

def getMainArgs():
    return (mainJSON['textKey'],mainJSON['name'],mainJSON['description'],)

def update(target):
    tk = mainJSON['textKey']
    feature = {}
    feature.update(mainJSON)
    feature['document'] = [
        {"type":"meta", "data": meta.decode('utf-8'), "single":True},
	    {"type":"installation", "data": installation.decode('utf-8'), "single":True},
    ]
    for (name, eventDoc) in events:
        feature['document'].append({"type":"event","name":name, "data":eventDoc.decode('utf-8'), "single":False})

    for (name, dashboardDoc) in dashboards:
        feature['document'].append({"type":"dashboard","name":name, "data":dashboardDoc.decode('utf-8'), "single":False})

    target[tk] = feature
"""
def string_to_byte_array_constant(string):
    byte_array = string.encode('utf-8')
    byte_array_constant = ', '.join(f'0x{byte:02x}' for byte in byte_array)
    return f'bytearray([{byte_array_constant}])'

def strip_unused_metrics(doc):
    updated_doc = doc
    if 'widgets' in updated_doc:
        for widget in updated_doc['widgets']:
            if 'option' in widget:
                option = widget['option']
                if 'metrics' in option:
                    target_metrics_idx = option['metrics']
                    option['metrics'] = 0
            
                    if 'metrics' in widget:
                        metrics = widget['metrics']
                        if len(metrics) > target_metrics_idx:
                            updated_metrics = [metrics[target_metrics_idx]]                            
                            widget['metrics'] = updated_metrics

    return updated_doc

import os
def debug_to_file(filename, doc):
    # 파일 이름에 "_modified"를 추가
    name, ext = os.path.splitext(filename)
    modified_filename = f"{name}_modified{ext}"
    
    # 파일에 doc 내용을 작성
    with open(modified_filename, 'w') as file:
        file.write(doc)

def write_module(source_files, target_file):
    with open(target_file, 'w', encoding='utf-8') as f:
        for (attrname, source_file) in source_files:
            if attrname == "dashboards":
                f.write(f'{attrname}=[')
                    
                for subfile in source_file:
                    dashboardjson = open(subfile, 'r').read()
                    name = json.loads(dashboardjson)['name']
                    f.write(f'\n("{name}",')
                    f.write(string_to_byte_array_constant(json.dumps(strip_unused_metrics(json.loads(dashboardjson)))))
                    f.write('),\n')
                    debug_to_file(subfile,json.dumps(strip_unused_metrics(json.loads(dashboardjson))))

                f.write(']\n')
            elif attrname == "events":    
                f.write(f'{attrname}=[')
                
                for (name, subfile) in source_file:
                    processed_events = []
                    events = json.loads(open(subfile, 'r').read())
                    for event in events:
                        process_event = {k: v for k, v in event.items() if k not in ("id", "receiver", "event_level_text", "eventLevelText", 'event_level')}
                        
                        process_event['eventLevel'] = 30
                        processed_events.append(process_event)
                    
                    f.write(f'\n("{name}",')
                    f.write(string_to_byte_array_constant(json.dumps(processed_events)))
                    f.write('),\n')
                f.write(']\n')
            else :
                f.write(f'{attrname}=')
                f.write(string_to_byte_array_constant(json.dumps(json.loads(open(source_file, 'r').read()))))
                f.write('\n')
            
        f.write(f"{getDefaultFunc()}\n")

def kafka():
    source_files = [
        ("main","kafka/main.json"),
        ("meta","kafka/meta.json"),
        ("installation","kafka/installation.json"),
        ("dashboards",("kafka/dashboard_default.json",
                                   "kafka/dashboard_broker.json",
                                   "kafka/dashboard_request.json"
                                   )),
        ("events",[("COMPOSITE_METRICS","kafka/event_composite_metrics.json")])
        ]
    target_file = "whfeature/features/kafka.py"
    write_module(source_files, target_file)

def vcenter():
    source_files = [
        ("main","vcenter/main.json"),
        ("meta","vcenter/meta.json"),
        ("installation","vcenter/installation.json"),
        ("dashboards",("vcenter/vHost Performance Overview.json",
                                   "vcenter/VMGuest Performance Overview.json",
                                   "vcenter/VMware Datastore.json",
                                   "vcenter/VMware Hosts.json",
                                   "vcenter/VMware Summary.json",
                                   )),
        ("events",[("METRICS","vcenter/event_doc.json")])
        ]
    target_file = "whfeature/features/vcenter.py"
    write_module(source_files, target_file)


def aerospike():
    source_files = [
        ("main","aerospike/main.json"),
        ("meta","aerospike/meta.json"),
        ("installation","aerospike/installation.json"),
        ("dashboards",("aerospike/overview.json",)),
        ("events",[("METRICS","aerospike/event-rules-matrics.json")])
        ]
    target_file = "whfeature/features/aerospike.py"
    write_module(source_files, target_file)


def apachepulsar():
    source_files = [
        ("main","apache_pulsar/main.json"),
        ("meta","apache_pulsar/meta.json"),
        ("installation","apache_pulsar/installation.json"),
        ("dashboards",("apache_pulsar/apachepulsar_overview.json",
                       "apache_pulsar/apachepulsar_overview_ii.json",
                       "apache_pulsar/apachepulsar_backlog.json",)),
        ("events",[])
        ]
    target_file = "whfeature/features/apachepulsar.py"
    write_module(source_files, target_file)

def nginx():
    source_files = [
        ("main","nginx/main.json"),
        ("meta","nginx/meta.json"),
        ("installation","nginx/installation.json"),
        ("dashboards",("nginx/nginx_overview.json",)),
        ("events",[])
        ]
    target_file = "whfeature/features/nginx.py"
    write_module(source_files, target_file)

def apache():
    source_files = [
        ("main","apache/main.json"),
        ("meta","apache/meta.json"),
        ("installation","apache/installation.json"),
        ("dashboards",("apache/apache_overview.json",
                       "apache/apache_throughput.json",
                       "apache/apache_worker_performance.json")),
        ("events",[])
        ]
    target_file = "whfeature/features/apache.py"
    write_module(source_files, target_file)


def milvus():
    source_files = [
        ("main","milvus/main.json"),
        ("meta","milvus/meta.json"),
        ("installation","milvus/installation.json"),
        ("dashboards",("milvus/milvus_proxy_and_root_coordinator.json",
                       "milvus/milvus_query_coordinator_query_node_metrics.json",
                       "milvus/milvus_search_and_compute_performance.json",)),
        ("events",[])
        ]
    target_file = "whfeature/features/milvus.py"
    write_module(source_files, target_file)

if __name__ == '__main__':
    #kafka()
    vcenter()
    #aerospike()
    #apachepulsar()
    #nginx()
    #apache()
    # milvus()