import yaml
import logging

from invoke import task
from collections import OrderedDict

logger = logging.getLogger('generator')

@task(help={'input-file': "A relative path to a valid .yml file",
            'output-file': "A relative path to output the template",
            })
def generate_aws_sam_template(ctx, input_file, output_file):
    """
    Takes a .yml input file with lambda definitions and outputs an AWS SAM cloudformation template
    """
    try:
        input = open(input_file).read()
    except IOError as e:
        logger.error(f'Could not read {input_file}: {e} ')
        raise e

    input_yaml = yaml.load(input)
    logger.debug(f'Received {input_yaml}')

    Helper.validate_input_yaml(input_yaml)

    # Start outputting the template file
    lambdas = {}
    # for each lambda in the file, create the lambda resource.
    for lambda_function in input_yaml['lambda_functions']:
        # OrderedDicts are used to dictate the order of the outgoing yml file
        lambdas[lambda_function['function_name']] = OrderedDict()
        lambdas[lambda_function['function_name']]['Type'] = 'AWS::Serverless::Function'
        lambdas[lambda_function['function_name']]['Properties'] = OrderedDict()
        lambdas[lambda_function['function_name']]['Properties']['Handler'] = lambda_function['handler']
        lambdas[lambda_function['function_name']]['Properties']['Runtime'] = lambda_function['runtime']
        lambdas[lambda_function['function_name']]['Properties']['CodeUri'] = lambda_function['code_uri']

    data = OrderedDict(
        AWSTemplateFormatVersion='2010-09-09',
        Transform='AWS::Serverless-2016-10-31',
        Description='A hello world application.',
        Resources=lambdas
    )

    # This ugly line tells pyyaml how to handle ordereddict
    yaml.add_representer(OrderedDict,
                         lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

    with open(output_file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


class Helper:

    @classmethod
    def validate_input_yaml(cls, input_yaml):
        """
        Validate yaml. If this were more complex, something like yamale could be used to
        put a schema on this
        :param input_yaml:
        :return:
        """
        # these keys must exist for each lambda provided
        required_keys = ['function_name', 'handler', 'code_uri', 'runtime']

        if 'lambda_functions' not in input_yaml:
            raise SchemaValidationException("invalid schema")

        # check each lambda function
        for lambda_function in input_yaml['lambda_functions']:
            # if any required key not in lambda input, throw an error
            if any(key not in lambda_function for key in required_keys):
                raise SchemaValidationException("invalid schema")

            # last but not least, make sure python2.7 is wiped from this earth
            if lambda_function['runtime'] == 'python2.7':
                raise UseABetterPythonVersionException("Please use at least python 3.6")


class SchemaValidationException(Exception):
    pass


class UseABetterPythonVersionException(Exception):
    pass
