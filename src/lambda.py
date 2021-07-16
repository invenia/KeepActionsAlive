#!/usr/bin/env python

import boto3
import json
import os

import keep_actions_alive


# Specifically gets parameters for running in a Lambda
def get_parameters():
    sm_client = boto3.client("secretsmanager")
    secret_key = os.getenv("GH_LOGIN_OR_TOKEN_KEY")
    login_or_token = json.loads(
        sm_client.get_secret_value(SecretId=secret_key)["SecretString"]
    )["Personal Access Token"]
    return {
        "login_or_token": login_or_token,
        "organization": os.getenv("GH_ORGANIZATION"),
    }


# Lambda entry point.  Does not use `event` and `context`
def lambda_handler(*kwargs):
    keep_actions_alive.keep_actions_alive(get_parameters())


# mainly for testing
if __name__ == "__main__":
    lambda_handler()
