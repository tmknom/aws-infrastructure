package ec2

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/ec2"

	. "../constant"
)

type Ec2Instance struct {
	Ec2Api ec2.EC2
}

type Ec2InstanceParam struct {
	ImageId                       string
	KeyName                       string
	SubnetId                      string
	SshSecurityGroupId            string
	InitializationSecurityGroupId string
}

type PublicIpAddress string

func (p PublicIpAddress) String() string {
	return string(p)
}

type InstanceId string

func (i InstanceId) String() string {
	return string(i)
}

func (ei Ec2Instance) Create(param Ec2InstanceParam) (InstanceId, PublicIpAddress, error) {
	fmt.Println("Launching a source AWS instance...")

	input := ei.createRunInstancesInput(param)
	resp, err := ei.runInstances(input)
	instance := resp.Instances[0]

	fmt.Println("Waiting for instance to become ready...")
	waitInput := ei.createDescribeInstanceStatusInput(instance)
	ei.waitUntilInstanceStatusOk(waitInput)

	instanceId := InstanceId(*(instance.InstanceId))
	publicIpAddress := PublicIpAddress(*(ei.getPublicIpAddress(instanceId)))

	return instanceId, publicIpAddress, err
}

func (ei Ec2Instance) runInstances(input *ec2.RunInstancesInput) (*ec2.Reservation, error) {
	return ei.Ec2Api.RunInstances(input)
}

func (ei Ec2Instance) createRunInstancesInput(param Ec2InstanceParam) *ec2.RunInstancesInput {
	runInstancesInput := &ec2.RunInstancesInput{
		ImageId:      aws.String(param.ImageId),
		MaxCount:     aws.Int64(1),
		MinCount:     aws.Int64(1),
		InstanceType: aws.String(BASE_INSTANCE_TYPE),
		IamInstanceProfile: &ec2.IamInstanceProfileSpecification{
			Name: aws.String(INITIALIZATION_INSTANCE_PROFILE),
		},
		BlockDeviceMappings: []*ec2.BlockDeviceMapping{
			{
				DeviceName: aws.String("/dev/xvda"),
				Ebs: &ec2.EbsBlockDevice{
					DeleteOnTermination: aws.Bool(true),
					VolumeSize:          aws.Int64(int64(BASE_VOLUME_SIZE)),
					VolumeType:          aws.String("gp2"),
				},
			},
		},
		NetworkInterfaces: []*ec2.InstanceNetworkInterfaceSpecification{
			{
				AssociatePublicIpAddress: aws.Bool(true),
				DeleteOnTermination:      aws.Bool(true),
				DeviceIndex:              aws.Int64(0),
				SubnetId:                 aws.String(param.SubnetId),
				Groups: []*string{
					aws.String(param.InitializationSecurityGroupId),
					aws.String(param.SshSecurityGroupId),
				},
			},
		},
	}

	if param.KeyName != "" {
		runInstancesInput.KeyName = aws.String(param.KeyName)
	}

	return runInstancesInput
}

func (ei Ec2Instance) waitUntilInstanceStatusOk(input *ec2.DescribeInstanceStatusInput) {
	ei.Ec2Api.WaitUntilInstanceStatusOk(input)
}

func (ei Ec2Instance) createDescribeInstanceStatusInput(instance *ec2.Instance) *ec2.DescribeInstanceStatusInput {
	return &ec2.DescribeInstanceStatusInput{
		InstanceIds: []*string{aws.String(*(instance.InstanceId))},
	}
}

func (ei Ec2Instance) Stop(instanceId InstanceId) {
	fmt.Println("Stopping the source instance...")
	input := ei.createStopInstancesInput(instanceId)
	ei.stopInstances(input)

	fmt.Println("Waiting for the instance to stop...")
	waitInput := ei.createDescribeInstancesInput(instanceId)
	ei.waitUntilInstanceStopped(waitInput)
}

func (ei Ec2Instance) stopInstances(input *ec2.StopInstancesInput) (*ec2.StopInstancesOutput, error) {
	return ei.Ec2Api.StopInstances(input)
}

func (ei Ec2Instance) createStopInstancesInput(instanceId InstanceId) *ec2.StopInstancesInput {
	return &ec2.StopInstancesInput{
		InstanceIds: []*string{
			aws.String(instanceId.String()),
		},
	}
}

func (ei Ec2Instance) Terminate(instanceId InstanceId) {
	fmt.Println("Terminating the source AWS instance...")
	input := ei.createTerminateInstancesInput(instanceId)
	ei.terminateInstances(input)
}

func (ei Ec2Instance) terminateInstances(input *ec2.TerminateInstancesInput) (*ec2.TerminateInstancesOutput, error) {
	return ei.Ec2Api.TerminateInstances(input)
}

func (ei Ec2Instance) createTerminateInstancesInput(instanceId InstanceId) *ec2.TerminateInstancesInput {
	return &ec2.TerminateInstancesInput{
		InstanceIds: []*string{
			aws.String(instanceId.String()),
		},
	}
}

func (ei Ec2Instance) waitUntilInstanceStopped(input *ec2.DescribeInstancesInput) {
	ei.Ec2Api.WaitUntilInstanceStopped(input)
}

func (ei Ec2Instance) getPublicIpAddress(instanceId InstanceId) *string {
	input := &ec2.DescribeInstancesInput{
		InstanceIds: []*string{
			aws.String(instanceId.String()),
		},
	}
	resp, _ := ei.describeInstances(input)
	return resp.Reservations[0].Instances[0].PublicIpAddress
}

func (ei Ec2Instance) describeInstances(input *ec2.DescribeInstancesInput) (*ec2.DescribeInstancesOutput, error) {
	return ei.Ec2Api.DescribeInstances(input)
}

func (ei Ec2Instance) createDescribeInstancesInput(instanceId InstanceId) *ec2.DescribeInstancesInput {
	return &ec2.DescribeInstancesInput{
		InstanceIds: []*string{aws.String(instanceId.String())},
	}
}
