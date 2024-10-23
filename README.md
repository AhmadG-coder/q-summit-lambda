# Workshop Resources

This repository contains the resources for the Mocking in Software Development workshop and DevOps.

## Slides

- [Link to Slides](https://docs.google.com/presentation/d/1x1xGOwn79n8iACELSSIuXbmP5oxBfys5/edit#slide=id.g30bc8e4984e_0_26)

## Code Examples

- [Source Code](lambda_function.py)
- [Test Cases](tests.py)
- [Deployment code](main.tf) 

## Requirements
- Terraform: for Deploying the lambda
- Python: for running the unit-tests

## Setup Instructions
```
terraform init
Terraform apply
pip install -r requirements.txt
pytest tests.py
```

## Additional Resources

- [Pytest](https://docs.pytest.org/en/7.3.x/)
- [Mock Object](https://docs.python.org/3/library/unittest.mock.html)
- [Mocking best-practices](https://www.telerik.com/blogs/mocking-best-practices)
- [Jenkins](https://www.jenkins.io/)
- [Terraform](https://www.terraform.io/)
- [Docker](https://docs.docker.com/get-started/)

## License

This project is licensed under the [MIT License](LICENSE).
