from django import template
from django.db.models import Count
from testApp.models import Post,comment
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def most_comment_post():
    post = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    return post
    
@register.simple_tag
def Latest_post():
    post = Post.objects.order_by('-publish')[0:2]
    return post
    
@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)

@register.filter(name='read_more')
@stringfilter
def read_more(value):
    pattern = "<!--more-->"
    return value.split(pattern, 1)[0]