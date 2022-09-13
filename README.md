# Django Visit Count

[![](https://img.shields.io/pypi/v/django-visit-count.svg)](https://pypi.python.org/pypi/django-visit-count/)
[![](https://img.shields.io/github/license/QueraTeam/django-visit-count.svg)](https://github.com/QueraTeam/django-visit-count/blob/master/LICENSE)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Count visits using cache for Django models.

## Installation

1. [Set-up](https://docs.djangoproject.com/en/dev/topics/cache/#setting-up-the-cache) Django's cache framework.

2. Install the Python package.

   ```
   pip install django_visit_count
   ```

## Usage

Use `VisitCountMixin`. It adds a `visit_count` field to your model.

```python
class MyBlogPost(VisitCountMixin, models.Model):
    ...
```

Count visits in your view like this:

```python
def view_blog_post(request, post_id):
    post = get_object_or_404(MyBlogPost, pk=post_id)
    post.update_visit_count()
    ...
```

## Advanced Usage

If you need more control, you can use `is_new_visit` function.

```python
class MyBlogPost(models.Model):
    total_visits = models.PositiveIntegerField(default=0)
    ...

def view_blog_post(request, post_id):
    post = get_object_or_404(MyBlogPost, pk=post_id)

    if is_new_visit(request, post):
        post.total_visits = F("total_visits") + 1
        post.save(update_fields=["total_visits"])

    ...
```

## Development

- Install development dependencies in your virtualenv with `pip install -e '.[dev]'`
- Install pre-commit hooks using `pre-commit install`.

## License

MIT