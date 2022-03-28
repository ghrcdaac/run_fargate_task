#! /usr/bin/env python3
import argparse
import boto3
from dataclasses import dataclass

@dataclass
class RunTaskInFargate:
    region_name: str= "us-west-2"

    def get_security_groups(self, ec2_name_filter):
        """
        Get All security group attached to EC2 instances
        boto3_ec2_client: boto3 ec2 client instance
        ec2_name_filter: EC2 name filter you want to get the security group from
        return: list of security groups
        """
        ec2_client = boto3.client('ec2', region_name=self.region_name)
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

    def get_subnets(self, subnet_name_filter):
        """
        Get All subnets ids with tag name containing the subnet_name_filter value
        boto3_ec2_client: boto3 ec2 client instance
        subnet_name_filter: Subnet tag name filter
        return: list of subnets ids
        """
        ec2_client = boto3.client('ec2', region_name=self.region_name)
        sn_all = ec2_client.describe_subnets()
        subnets_ids = []
        for sn in sn_all['Subnets']:
            for tag in sn['Tags']:
                if subnet_name_filter in tag['Value']:
                    subnets_ids.append(sn['SubnetId'])
        return subnets_ids

    def run_task_in_fargate(self, cluster_name, task_definition_name, command,
                            ec2_name_filter="*CumulusECSCluster", subnet_name_filter="Private application",
                            task_name="IMSCorrection"):

        security_groups = self.get_security_groups(ec2_name_filter = ec2_name_filter)
        subnets = self.get_subnets(subnet_name_filter=subnet_name_filter)

        ecs_client = boto3.client('ecs', region_name=self.region_name)
        networkConfiguration = {
        'awsvpcConfiguration': {
            'subnets': subnets,
            'securityGroups': security_groups,
            'assignPublicIp': 'DISABLED'
            }
        }
        response = ecs_client.run_task(cluster=cluster_name,
                               launchType='FARGATE',
                               overrides={'containerOverrides': [{'name': task_name,'command': command}]},
                               networkConfiguration=networkConfiguration,
                               taskDefinition=task_definition_name)
        return response

    @classmethod
    def cli(cls):

        parser = argparse.ArgumentParser(description='This script will run an activity in a fargate')
        parser.add_argument('-aws_profile', '--aws_profile', dest='aws_profile', nargs=1, required=True,
                        help='AWS profile')
        parser.add_argument('-cmd', '--command', dest='cmd', nargs=1, required=True,
                        help='command to run')
        parser.add_argument('-p', '--prefix', dest='prefix', nargs=1, required=True,
                        help='Cumulus stack prefix')
        args = parser.parse_args()

        profile_name, cmd, stack_prefix = args.aws_profile[0],args.cmd[0].split(), args.prefix[0]

        cluster_name = f'{stack_prefix}-CumulusECSCluster'
        task_definition_name = f'{stack_prefix}-CorrectIMSTaskDefinition'
        client = cls()
        boto3.setup_default_session(profile_name=profile_name)
        response = client.run_task_in_fargate(cluster_name=cluster_name, task_definition_name=task_definition_name,
                                              command=cmd)
        print(response)
