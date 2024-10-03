### Step 0: 根據需求修改create_network_policy.yaml
修改LDAP 端點位置，namespace 名稱，licensed user 數量

### Step 1: 使用docker build 製作container image 並在本機端推到偏好的repository

### Step 2: 放置必要assets 至 site-config
複製arke-deploy-license.yaml/ networkpolicy.yaml/ arke-role-license.yaml 放置到site-config/license_protector  底下
並修改NS / image / repo 名稱

### Step 3: 修改kustomization.yaml
在kustomize 中的resources 欄位加上reference
```
resources:
## add  the networkpolciy to forbid the access to sas-logon
- site-config/networkpolicy.yaml

transformers:
## add license checker container on sas-arke deployment
- site-config/license_protector/arke-deploy-license.yaml

## grant arke networkpolicy permission
- site-config/license_protector/arke-role-license.yaml

```
### Step 4: 增加patchTransformer 改寫sas-arke deployment


