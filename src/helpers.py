def get_security_groups(boto3_ec2_client, ec2_name_filter):
    """
    Get All security group attached to EC2 instances
    boto3_ec2_client: boto3 ec2 client instance
    ec2_name_filter: EC2 name filter you want to get the security group from
    return: list of security groups
    """
    ec2_all = ec2_client.describe_instances(Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                ec2_name_filter,
            ]
        },
    ])
    sgs = []
    for inst in ec2_all['Reservations']:
        for rec in inst['Instances']:
            for sub in rec['SecurityGroups']:
                sgs.append(sub['GroupId'])

    sgs = list(set(sgs))
    return sgs

def get_subnets(boto3_ec2_client, subnet_name_filter):
    """
    Get All subnets ids with tag name containing the subnet_name_filter value
    boto3_ec2_client: boto3 ec2 client instance
    subnet_name_filter: Subnet tag name filter
    return: list of subnets ids
    """
    sn_all = ec2_client.describe_subnets()
    subnets_ids = []
    for sn in sn_all['Subnets']:
        for tag in sn['Tags']:
            if subnet_name_filter in tag['Value']:
                subnets_ids.append(sn['SubnetId'])
    return subnets_ids