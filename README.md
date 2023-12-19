[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![linters](https://github.com/DukeOfRI/flask-authorizer/actions/workflows/pipeline.yml/badge.svg)

# Introduction
This code can be used to efficiently handle authorization in a Flask application. It is fully decoupled from 
authentication. Therefore, you can use any authentication method you want (Azure AD, username/password, etc.). This
package is inspired by some existing open-source packages for authorization.

# Installation
The package can be installed using pip. Simply run the command below:

```pip install ...```

Python 3.11 and pyton 3.12 are supported.


> **NOTE:** The wrapper indicating the Flask route should come <u>**before**</u> the wrapper for authorization. 
> Otherwise, authorization will not be executed. For example:
> 
> ```python
> @app.route("/")
> @authorizer.requires_permission(user_can_view)
> def hello_world():
>     return "<p>Hello World!</p>"
> ```


# Benefits
- Works with any authentication method. Strict separation of responsibilities. Authentication and authorization are decoupled.
- Easy to implement in your (existing) flask application using 1 line of code per endpoint.


# Example
```python
from flask_authorizer import Authorizer

def load_user():
    """Business logic for loading user (authentication) goes here."""
    return {"name": "Joe Example", "permissions": ["view", "delete"]}

def forbidden():
    """Function to be run when authorization fails"""
    return "forbidden"

def user_can_delete_project(user):
    return "delete" in user["permissions"]

authorizer = Authorizer(load_user, forbidden)

@authorizer.requires_permission(user_can_delete_project)
def delete_project():
    return "project deleted"
```