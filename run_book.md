# **HealthSync Run Book**  
## **Application for Managing Patient Health Records and Appointments**  

---

## **1. Repository Setup**  

### **Clone the Repository**  
```cmd
git clone https://github.com/veensew/meditrack.git
cd healthsync
```

---

## **2. Environment Variables**  
Environment variables are stored securely in the GitHub repository secrets:
- **GKE_PROJECT**
- **GKE_SA_KEY**
- **MONGO_URL**
- **REDSHIFT_DB**
- **REDSHIFT_HOST**
- **REDSHIFT_USER**
- **REDSHIFT_PASSWORD**
- **SMTP_USERNAME**
- **SMTP_PASSWORD**

These will automatically be loaded in the cloud environment during CI/CD pipeline execution.

---

## **3. CI/CD Pipeline with GitHub Actions**  
All builds, deployments, and tests will run in the cloud environment using GitHub Actions workflows. 

### **GitHub Actions Workflow**  
Located in `.github/workflows/deploy.yml`. Key steps:
- **Build**: Python services for each microservice.
- **Deploy**: Use `gcloud` CLI and `kubectl` to deploy to GKE.
- **Test**: Run integration tests in the cloud environment.

---

## **4. Deploying to Google Kubernetes Engine (GKE)**  

All deployments are handled by the CI/CD pipeline. The Kubernetes manifests for each microservice are located in the `kubernetes` directory. GitHub Actions will apply these manifests to the GKE cluster.

### **Deployment Steps** (automated in CI/CD):  
```cmd
gcloud container clusters get-credentials meditrack-cluster --region=<region>
kubectl apply -f kubernetes/
```

### **Verify Deployment**  
To verify deployment from the cloud environment:  
```cmd
kubectl get pods
kubectl get services
```

---

## **5. Observability**  

### **Cloud Monitoring**  
Google Cloud provides built-in observability for GKE:  
- **Cloud Logging** for centralized logs.
- **Cloud Monitoring** for metrics, health checks, and alerts.

Access these features via the **Google Cloud Console** under the GKE cluster monitoring section.

---

## **6. AWS Redshift and QuickSight Integration**  

1. Aggregated data is automatically exported to **AWS Redshift** during the deployment process.
   - Credentials and endpoints are configured using repository secrets:
     - **REDSHIFT_HOST**, **REDSHIFT_DB**, **REDSHIFT_USER**, **REDSHIFT_PASSWORD**
2. Use **AWS QuickSight** to visualize Redshift data with dashboards.

---

## **7. Testing and Debugging in the Cloud**  

### **Run Integration Tests**  
Integration tests are run during the CI/CD pipeline execution in the cloud environment using `pytest`. No local testing is required.

---

## **8. Common Kubernetes Commands for Cloud Debugging**  
Run these commands if debugging directly in the GKE cluster:
- **Get All Pods**:  
```cmd
kubectl get pods
```
- **Describe Deployment**:  
```cmd
kubectl describe deployments
```
- **Check Service Status**:  
```cmd
kubectl get services
```
- **Restart a Deployment**:  
```cmd
kubectl rollout restart deployment/<service-name>
```

---

## **9. Deleting and Cleaning Up**  

### **Delete Kubernetes Deployments**  
```cmd
kubectl delete deployments --all
kubectl delete services --all
kubectl delete pods --all
```

### **Delete GKE Cluster**  
```cmd
gcloud container clusters delete meditrack-cluster --region=<region>
```
