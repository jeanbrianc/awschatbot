import boto3
from botocore.exceptions import BotoCoreError, ClientError
from langchain.tools import tool
from typing import Optional


def _s3_client():
    return boto3.client("s3")


def _ec2_client():
    return boto3.client("ec2")


def _iam_client():
    return boto3.client("iam")


@tool("count_public_s3_buckets")
def count_public_s3_buckets() -> str:
    """Return the number of S3 buckets that are publicly accessible."""
    s3 = _s3_client()
    try:
        response = s3.list_buckets()
    except (BotoCoreError, ClientError) as e:
        return f"Failed to list buckets: {e}"

    buckets = response.get("Buckets", [])
    public_buckets = []
    for b in buckets:
        name = b["Name"]
        try:
            acl = s3.get_bucket_acl(Bucket=name)
        except ClientError as e:
            continue
        for grant in acl.get("Grants", []):
            grantee = grant.get("Grantee", {})
            uri = grantee.get("URI", "")
            if "AllUsers" in uri or "AuthenticatedUsers" in uri:
                public_buckets.append(name)
                break
    return str(len(public_buckets))


@tool("describe_bucket_contents")
def describe_bucket_contents(bucket: str) -> str:
    """Return a short description of the objects stored in the S3 bucket."""
    s3 = _s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
    except (BotoCoreError, ClientError) as e:
        return f"Failed to list contents of {bucket}: {e}"
    contents = response.get("Contents", [])
    if not contents:
        return f"Bucket {bucket} is empty."
    keys = [obj["Key"] for obj in contents]
    return "\n".join(keys)


@tool("ec2_instance_type_by_ip")
def ec2_instance_type_by_ip(ip: str) -> str:
    """Given an IP address, return the instance type of the EC2 instance."""
    ec2 = _ec2_client()
    try:
        resp = ec2.describe_instances(
            Filters=[{"Name": "ip-address", "Values": [ip]}, {"Name": "private-ip-address", "Values": [ip]}]
        )
    except (BotoCoreError, ClientError) as e:
        return f"Failed to describe instances: {e}"
    for reservation in resp.get("Reservations", []):
        for inst in reservation.get("Instances", []):
            return inst.get("InstanceType", "unknown")
    return "Instance not found"


@tool("describe_user_permissions")
def describe_user_permissions(user: str) -> str:
    """Return list of attached IAM policies for the given user."""
    iam = _iam_client()
    try:
        attached = iam.list_attached_user_policies(UserName=user)
        inline = iam.list_user_policies(UserName=user)
    except (BotoCoreError, ClientError) as e:
        return f"Failed to describe user {user}: {e}"
    policies = [p["PolicyName"] for p in attached.get("AttachedPolicies", [])]
    policies.extend(inline.get("PolicyNames", []))
    if not policies:
        return f"User {user} has no policies."
    return "\n".join(policies)
