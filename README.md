[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![linters](https://github.com/DukeOfRI/flask-authorizer/actions/workflows/pipeline.yml/badge.svg)

# Introduction
This code can be used to efficiently handle authorization in a Flask application. It is fully decoupled from 
authentication. Therefore, you can use any authentication method you want (Azure AD, username/password, etc.).

# Installation


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