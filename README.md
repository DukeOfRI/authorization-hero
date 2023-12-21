<p>
  <img src="https://github.com/DukeOfRI/flask-authorizer/actions/workflows/pipeline.yml/badge.svg" alt="Build" />
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
</p>

# Authorization

Add authorization to your Flask application in 1 line per endpoint!

This package can be used to efficiently handle authorization in a Flask application. It is fully decoupled from
authentication. Therefore, you can use any authentication method you want (Azure AD, username/password, etc.).

Authorization is checked each time an endpoint is requested. It is up to the developer to implement a method
to identify the user (authentication) and load user authorizations. One is free to cache authentication data or reload
it upon each request. It is up to the developer to find a good tradeoff between security (always reload) and
performance (cache).

- This package fully supports Role-based access control (**RBAC**). This authorization method is mostly used in
  enterprise settings.
- The package also supports Attribute-based access control (**ABAC**) which is an extension of RBAC, but also includes
  other attributes.
    - For example, one could check that a user is part of a certain group AND is over 18.
    - One could check that a user is part of a certain group AND only allow access to an endpoint during working hours.
    - One could only allow access to an endpoint when the user has been registered for more than 1 month.

Python 3.11 and Pyton 3.12 are supported.

FastAPI support will be added in a future release.

# Installation

The package can be installed using pip. Simply run the command below.

```pip install flask-authorizer```

# How to use

To incorporate authorization into your codebase, start by importing the `Authorizer` class. Next, create two functions:
one to load the user and another to be executed when an endpoint is forbidden for a user.

Now, create a function to handle your authorization logic. This function should take the user as its only input
argument.

For each endpoint in your application, add a decorator to check whether the user has a certain permission.

```python
from flask import Flask, abort

from authorization import Authorizer


def flask_forbidden():
    abort(403, "Forbidden: you do not have access to this resource")


def load_user() -> dict:
    """Business logic for authentication goes here"""
    return {"name": "Joe Example", "permissions": ["view", "edit"]}


def user_can_view(user: dict) -> bool:
    return 'view' in user["permissions"]


app = Flask(__name__)
authorizer = Authorizer(load_user, flask_forbidden)


@app.route("/")
@authorizer.requires_permission(user_can_view)
def hello_world():
    return "<p>Hello World!</p>"
```

The order of the wrappers matters!

> **NOTE:** The wrapper indicating the Flask route must come <u>**before**</u> the wrapper for authorization.
> Otherwise, authorization will not be executed. So, use the order below.
>
> ```python
> @app.route("/")
> @authorizer.requires_permission(user_can_view)
> def hello_world():
>     return "<p>Hello World!</p>"
> ```

# Additional requirements

To initialize the `Authorizer` class, two input parameters are required: `identity_loader` and `on_forbidden`. Both
must be functions and must adhere to the following conditions:

- The `identity_loader` function must have no input parameters and should return user data.
- The `on_forbidden` function must have no input parameters.
- Each authorization function must take exactly one input parameter, which should be the return value of the
  `identity_loader` function.
- Each authorization function must return a boolean value indicating whether an endpoint is allowed or forbidden for the
  user.

The package is tested and adheres to the _black_ code style.
Have a look at the test suite for more suggestions on how to use this package.