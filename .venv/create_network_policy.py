import os, time
from kubernetes import client, config
from ldap3 import Server, Connection, ALL

def count_users(ldap_server, bind_dn, password):

    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, bind_dn, password, auto_bind=True)

    conn.search('dc=gelldap,dc=com', '(objectClass=posixAccount)', attributes=['cn'])

    return len(conn.entries)


def create_network_policy():
    # 載入 Kubernetes 配置
    config.load_incluster_config()  # 集群内部用 config.load_incluster_config()

    # 定義一 deny all 的 NetworkPolicy
    deny_all_policy = client.V1NetworkPolicy(
        api_version="networking.k8s.io/v1",
        kind="NetworkPolicy",
        metadata=client.V1ObjectMeta(
            name="deny-all-networkpolicy",
            namespace="viya4stable202302"  # 替換成viya 的namespace
        ),
        spec=client.V1NetworkPolicySpec(
            pod_selector=client.V1LabelSelector(
                match_labels={"app": "sas-logon-app"} # pod Selector 選擇Viya pods
            ),
            policy_types=["Ingress"]  # 拒絕所有訪問
        )
    )

    # 創建API 物件
    api_instance = client.NetworkingV1Api()

    # 嘗試獲取現行 NetworkPolicy
    try:
        existing_policy = api_instance.read_namespaced_network_policy(
            name="deny-all-networkpolicy",
            namespace="viya4stable202302"  # 替換為viya namespace
        )
        # 如果存在，更新NWP
        response = api_instance.replace_namespaced_network_policy(
            name="deny-all-networkpolicy",
            namespace="viya4stable202302",
            body=deny_all_policy
        )
        print("Deny All NetworkPolicy updated.")
    except client.exceptions.ApiException as e:
        print(e.status)
        if e.status == 404:
            # 如果不存在，創建NWP
            response = api_instance.create_namespaced_network_policy(
                namespace="viya4stable202302",  # 替换为viya namespace
                body=deny_all_policy
            )
            print("Deny All NetworkPolicy created.")
        else:
            print("Exception when checking NetworkPolicy")

def delete_network_policy():
    # 載入 Kubernetes 配置
    config.load_incluster_config()  # 集群内部用 config.load_incluster_config()
    # 創建API 物件
    api_instance = client.NetworkingV1Api()

    # 嘗試獲取現行 NetworkPolicy
    try:
        existing_policy = api_instance.read_namespaced_network_policy(
            name="deny-all-networkpolicy",
            namespace="viya4stable202302"  # 替換為viya namespace
        )
        # 如果存在，移除NWP
        response = api_instance.delete_namespaced_network_policy(
            name="deny-all-networkpolicy",
            namespace="viya4stable202302"
        )
        print("Deny All NetworkPolicy removed.")
    except client.exceptions.ApiException as e:
        print(f"Error occured while Removing NWP {e.status}")


if __name__ == "__main__":
    ldap_server = 'ldap://gelldap-service:389'
    bind_dn = 'cn=admin,dc=gelldap,dc=com'
    password = 'lnxsas'
    licensed_user = 2
    while True:
        total_users = count_users(ldap_server, bind_dn, password)
        print(f"total number of users: {total_users}")

        if total_users > licensed_user:
            print(f"actual user counts {total_users} is higher than the licensed user {licensed_user}")
            create_network_policy()
        else:
            print(f"actual user counts {total_users} is equal or lower than the licensed user {licensed_user}")
            delete_network_policy()

        time.sleep(30)







