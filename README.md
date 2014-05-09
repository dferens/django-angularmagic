# django-angularmagic


**Status: not implemented yet**

<a name="overview"/>
## Overview

Provides *{% angularapp %}* tag which simplifies integration of Angular views into complete Django apps.


<a name="example"/>
## Example

Assume next Django app:

```python
# models.py

from django.db import models

class BlogPost(models.Model):
    text = models.TextField()
  
class BlogPostComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name='comments')
    text = models.TextField()

# views.py

from django.views.generic import DetailView

from . import models

class BlogPostDetail(DetailView):
    model = models.BlogPost
    context_object_name = 'blogpost'
    template_name = 'blogpost_detail.html'
```

Now the most interesting:

1. Include *AngularJS* and module's directives:

    ```html
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.16/angular.js"></script>
    <script src="{% static 'angularmagic/angularmagic.js' %}"></script>
    ```

1. Include *{% angularapp %}* tag and pass some variables from current context:

    ```django
    {% load angularmagic %}
    
    {% angularapp 'blogpost' comments=blogpost.comments.all %}
    //
    //  View code goes here ...
    //
    {% endangularapp %}
    ```
    
    **Variables defined inside *{% angularapp %}* will not be evaluated by Django**, any other Django tags are still working though.
    
    (It's even possible to mix Django tags with Angular views but I'm not sure it's a good practice.)

1. Bind passed context to any Angular scope with *django-context* directive:

    ```html
    <div ng-controller="BlogPostCtrl" django-context>
    ```

1. Add your view code:
    
    ```django
    {% angularapp 'blogpost' comments=blogpost.comments.all %}
      <div ng-controller="MyCtrl" django-context>
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


<a name="requirements/">
## Requirements

* Python (2.6, 2.7, 3.2, 3.3)
* Django (1.4 - 1.6)


<a name="install"/>
## Installation

```bash
pip install django-angularmagic
```

<a name="config"/>
## Configuration

```python
INSTALLED_APPS = (
    ...
    'angularmagic',
)
```

## TODOs:

* Add *{% variable var_name %}* inclusion tag;
* Add support of serializers from rest-framework & tastypie;
