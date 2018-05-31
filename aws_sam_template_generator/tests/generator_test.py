import os, sys, shutil
import pytest
from invoke import Context

from aws_sam_template_generator.tasks import (generate_aws_sam_template,
                                              SchemaValidationException,
                                              UseABetterPythonVersionException)


def setup_module(module):
    # kill/create /tmp dir
    path = os.path.dirname(os.path.abspath(__file__)) + '/tmp'
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def test_one_lambda_correct_file():
    filename = 'test_templates/one-lambda.yml'
    path = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(path, filename)

    output_filename = 'tmp/one-lambda.yml'
    output_filename = os.path.join(path, output_filename)

    ctx = Context()
    generate_aws_sam_template(ctx, input_filename, output_filename)

    # verify the file got created, correctly
    actual_output_file = open(output_filename).read()

    assert actual_output_file == """AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: A hello world application.
Resources:
  HelloWorld:
    Type: AWS::Serverless::Function
    Properties:
      Handler: HelloWorld.main
      Runtime: python3.6
      CodeUri: lambda.zip
"""


def test_multiple_lambdas():
    filename = 'test_templates/multiple-lambdas.yml'
    path = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(path, filename)

    output_filename = 'tmp/multi-lambda.yml'
    output_filename = os.path.join(path, output_filename)

    ctx = Context()
    generate_aws_sam_template(ctx, input_filename, output_filename)

    # verify the file got created, correctly
    actual_output_file = open(output_filename).read()

    assert actual_output_file == """AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: A hello world application.
Resources:
  HelloWorld:
    Type: AWS::Serverless::Function
    Properties:
      Handler: HelloWorld.main
      Runtime: python3.6
      CodeUri: lambda.zip
  HelloWorld2:
    Type: AWS::Serverless::Function
    Properties:
      Handler: HelloWorld2.main
      Runtime: python3.6
      CodeUri: lambda2.zip
"""


def test_missing_keys():
    """ This explodes in a firey exception, that pytest expects"""
    filename = 'test_templates/missing-keys.yml'
    path = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(path, filename)

    output_filename = 'tmp/missing-keys.yml'
    output_filename = os.path.join(path, output_filename)

    ctx = Context()
    with pytest.raises(SchemaValidationException):
        generate_aws_sam_template(ctx, input_filename, output_filename)


def test_get_rid_of_old_python():
    """ 2.7 is evil. It must be expunged."""
    filename = 'test_templates/python2.7.yml'
    path = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(path, filename)

    output_filename = 'tmp/missing-keys.yml'
    output_filename = os.path.join(path, output_filename)

    ctx = Context()
    with pytest.raises(UseABetterPythonVersionException):
        generate_aws_sam_template(ctx, input_filename, output_filename)


def teardown_module(module):
    # Kill the /tmp dir
    path = os.path.dirname(os.path.abspath(__file__)) + '/tmp'
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)