from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from board.models import Profile, Post, JobType, Subscribe
from django_summernote.admin import SummernoteModelAdmin

class ProfileAdmin(AdminImageMixin, admin.ModelAdmin):
	list_display = ('user', 'companyName', 'description', 'website', 'contactName', 'contactEmail', 'logo')

class SubscribeAdmin(admin.ModelAdmin):
	list_display = ('name', 'email')

class JobTypeAdmin(admin.ModelAdmin):
	list_display = ('title',)

class PostAdmin(admin.ModelAdmin):
	list_display = ('profile', 'title', 'description', 'jobType', 'wage', 'publishDate', 'expirationDate', 'active', 'views')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(JobType, JobTypeAdmin)
