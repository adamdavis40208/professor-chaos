Feature: generate template

  Scenario: generating a template from yml
    Given A yml with a single lambda
    When the file is submitted to s3
    Then Template is returned with single lambda

    Given A yml with multiple lambdas
    When the file is submitted to s3
    Then Template is returned with multiple lambdas

    Given A yml with a single bad lambda
    When the file is submitted to s3
    Then An error condition is raised