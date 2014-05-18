# django-angularmagic

[![Build Status](https://travis-ci.org/dferens/django-angularmagic.svg?branch=master)](https://travis-ci.org/dferens/django-angularmagic)
[![Coverage Status](https://coveralls.io/repos/dferens/django-angularmagic/badge.png?branch=master)](https://coveralls.io/r/dferens/django-angularmagic?branch=master)

## Overview

Provides *{% angularapp %}* tag which simplifies integration of Angular views into complete Django apps.

## Requirements

* Python 2.6, 2.7, ~~3.2, 3.3~~
* Django 1.5+
* (optionally, [django-rest-framework](https://github.com/tomchristie/django-rest-framework))
* (optionally, [django-tastypie](https://github.com/toastdriven/django-tastypie))

## Example

Assume next Django app:

**models.py**:

```python
from django.db import models

class BlogPost(models.Model):
    text = models.TextField()
  
class BlogPostComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name='comments')
    text = models.TextField()
```

**views.py**:

```python
from django.views.generic import DetailView

from . import models

class BlogPostDetail(DetailView):
    model = models.BlogPost
    context_object_name = 'blogpost'
    template_name = 'blogpost_detail.html'
```

Now the most interesting:

1. Add *AngularMagicMixin* and describe inner context:

    ```python
    from django.views.generic import DetailView
    from angularmagic.views import AngularMagicMixin
    from . import models

    class BlogPostDetail(AngularMagicMixin, DetailView):
        model = models.BlogPost
        context_object_name = 'blogpost'
        template_name = 'blogpost_detail.html'

        def get_included_context(self, context):
            return {
                'blogpost': context['blogpost'],
                'comments': context['blogpost'].comments.all()
            }
    ```

1. Include *{% angularapp %}* tag:

    ```django
    {% load angularmagic %}
    
    {% angularapp %}
    //
    //  View code goes here ...
    //
    {% endangularapp %}
    ```
    
    **Variables defined inside *{% angularapp %}* will not be evaluated by Django**, any other Django tags are still working though.
    
    (It's even possible to mix Django tags with Angular views but I'm not sure it's a good practice.)

1. Bind passed context to any Angular scope with *bind-django-context* directive:

    ```html
    <div ng-controller="BlogPostCtrl" bind-django-context>
    ```

1. Add your view code:
    
    ```django
    {% angularapp %}
      <div ng-controller="MyCtrl" bind-django-context>
        {{ blogpost.text }}
        <div class="comment-holder">
          <div class="comment" ng-repeat="comment in comments">
            <p>{{ comment.text }}</p>
          </div>
        </div>
      </div>
    {% endangularapp %}
    ```

Everything will be evaluated by AngularJS.

## Installation

```python
INSTALLED_APPS = (
    ...
    'angularmagic',
)
```
```javascript
angular.module('myModule', ['django.angularmagic']);
```

Grab module with

```django
<script src="{% static 'angularmagic/angularmagic.js' %}"></script>
```

## Configuration

*AngularMagicMixin* provides next configuration variables:

1. serializer_classes

    You can specify how your models should be serialized with serializer classes.
    Both *Serializer* of *rest_framework* and *Resource* or *tastypie* are supported:
    
    **api.py**:
    
    ```python
    import rest_framework.serializers
    import tastypie.resources
    
    from . import models
    
    class BlogPostSerializer(rest_framework.serializers.ModelSerializer):
        class Meta:
            model = models.BlogPost


    class BlogPostCommentResource(tastypie.resources.ModelResource):
        class Meta:
            queryset = models.BlogPostComment.objects.all()

    ```
    
    **views.py**:
    
    ```python
    from django.views.generic import DetailView
    from angularmagic.views import AngularMagicMixin
    
    from . import api, models
    
    class BlogPostDetail(AngularMagicMixin, DetailView):
        ...
        # Can be a dict
        serializer_classes = {
            models.BlogPost: api.BlogPostSerializer,
            models.BlogPostComment: api.BlogPostCommentResource
        }
        # Or a list if each serializer/resource is model-related
        # (i.e. is a ``ModelResource`` or ``ModelSerializer`` subclass):
        serializer_classes = [BlogPostSerializer, BlogPostCommentResource]
    ```
    
    Or create your own serializers using [base classes](/angularmagic/base.py)

## TODOs:
* Add tests;
* (?) Add *{% variable var_name %}* inclusion tag;
* Add asynchronous context retrieval.
