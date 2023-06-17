# Workshop Resources

This repository contains the resources for the Mocking in Software Development workshop.

## Slides

- [Link to Slides](https://docs.google.com/presentation/d/e/2PACX-1vQuRqoUkwFirJ_6nFCGVyGiMrm2aAJm80qsiQNrQgLLarY-7PNs4LUCX2V1DC-fAnl9eSe7_G7gAd34/pub?start=false&loop=false&delayms=3000)

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

## License

This project is licensed under the [MIT License](LICENSE).