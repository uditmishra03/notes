## MULTI-TENANCY

### How in EKS cost is calculated for each NS?

#### If 10 teams share one EKS cluster, how would you track the cost of each namespace?

“In a multi-tenant EKS cluster, cost attribution is typically handled using namespace labeling combined with usage metrics. Each tenant namespace is labeled with a team or cost-center identifier. Tools like Kubecost then use Prometheus metrics to map CPU, memory, storage, and network consumption back to those namespaces and translate that into cloud infrastructure cost. For cloud resources such as EBS or load balancers, AWS cost allocation tags can also be used.”
