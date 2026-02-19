import json

data = '{"service":"auth","status":"running","instances":3}'


# print(type(data))

data_dict = json.loads(data)

# print(data_dict)

print(f"Service: {data_dict['service']}")
print(f"Status: {data_dict['status']}")
print(f"Instances: {data_dict['instances']}")
