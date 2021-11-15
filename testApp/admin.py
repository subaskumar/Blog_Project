from django.contrib import admin
from testApp.models import Post,comment,Profile,Foo
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','body','publish','created','updated','status')
    prepopulated_fields = {'slug':('title',)}   # The main use for this functionality is to automatically
                                    # generate the value for SlugField fields from one or more other fields.
    list_filter = ('status','author','publish','created')
    search_fields = ('title','body')
    #raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','created']

class commentAdmin(admin.ModelAdmin):
    list_display = ('Name','post','body','reply','created','updated','active')
    list_filter = ('created','updated','active','post')
    search_fields = ('Name','content')

class ProfileAdmin(admin.ModelAdmin):
    list_display= ('user','DOB','address','gender','bio')

class UserAdmin(admin.ModelAdmin):
    list_display= ('username','email','is_active')

class FooAdmin(admin.ModelAdmin):
    list_display = ['x','y','z','score']
    prepopulated_fields = {'score':('x','y','z')}
    
admin.site.register(Foo,FooAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(comment,commentAdmin)
admin.site.register(Profile,ProfileAdmin)
