#! /usr/bin/env python3
import argparse
import boto3
from dataclasses import dataclass
from helpers import get_security_groups, get_subnets

@dataclass
class RunTaskInFargate:
    profile_name: str
    cmd: str
        

    @staticmethod(f)
    def run_task_in_fargate(profile_name, cluster_name, task_definition_name, comand, region_name="us-west-2",
                        ec2_name_filter="*CumulusECSCluster", subnet_name_filter="Private application", task_name="RecordCorrection"):

        print(locals())
        return locals()

        boto3.setup_default_session(profile_name=profile_name)
        ec2_client = boto3.client('ec2', region_name=region_name)
        security_groups = get_security_groups(boto3_ec2_client=ec2_client, ec2_name_filter = ec2_name_filter)
        subnets = get_subnets(boto3_ec2_client=ec2_client, subnet_name_filter=subnet_name_filter)

        ecs_client = boto3.client('ecs', region_name=region_name)
        networkConfiguration = {
        'awsvpcConfiguration': {
            'subnets': subnets,
            'securityGroups': security_groups,
            'assignPublicIp': 'DISABLED'
            }
        }
        response = ecs_client.run_task(cluster=cluster_name,
                               launchType='FARGATE',
                               overrides={'containerOverrides': [{'name': task_name,'command': comand}]},
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
        response = run_fargate(profile_name=profile_name, command=cmd, stack_prefix=stack_prefix,
                cluster_name=cluster_name, task_definition_name=task_definition_name)
        print(response)
