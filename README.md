# django-angularmagic


**Status: not implemented yet**

<a name="overview"/>
## Overview

Provides *{% angularapp %}* tag which simplifies integration of Angular views into complete Django apps.

<a name="requirements/">
## Requirements

* ~~~Python (2.6, 2.7, 3.2, 3.3)~~~
* ~~~Django (1.4 - 1.6)~~~
* [https://github.com/tomchristie/django-rest-framework][django-rest-framework]

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

<a name="install"/>
## Installation

```bash
pip install django-angularmagic
```
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

## TODOs:
* Add tests;
* (?) Add *{% variable var_name %}* inclusion tag;
* Add support of serializers from rest-framework & tastypie;
