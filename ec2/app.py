import os
from aws_cdk import (
    core,
    aws_ec2 as ec2,
)


class FirstEc2(core.Stack):
    def __init__(self, scope: core.App, name: str, key_name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # VPCを定義
        vpc = ec2.Vpc(
            self,
            "FirstEc2-Vpc",
            max_azs=1,
            cidr="10.10.0.0./23",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        # Security Groupを定義
        # 任意にIPv4のアドレスからの、ポート22（SSH接続に使用されるポート）への接続を許可
        sg = ec2.SecurityGroup(
            self,
            "FirstEc2-Sg",
            vpc=vpc,
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )

        # VPCとSGが付与されたEC2インスタンスを作成
        host = ec2.Instance(
            self,
            "FirstEc2",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnet=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            key_name=key_name,
        )
