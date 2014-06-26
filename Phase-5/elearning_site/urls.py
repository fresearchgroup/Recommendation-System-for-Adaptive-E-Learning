from django.conf.urls import patterns, include, url
from reco_app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', login_form),
    url(r'^EvaluationWelcome/$',Evaluation_welcome),
    url(r'FeedbackEvaluation/$',Feedback_evaluation),
    url(r'MaterialEvaluation/$',Material_evaluation),
    url(r'EvaluationParameters/$',Parameter_evaluation),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login-form/$', login_form), 
    url(r'^login/$', login_handler), 
    url(r'^signup/$', registeration_form),
    url(r'^signup_handler/$', signup_handler),
    url(r'^logout/$', logout_handler), 
    url(r'^concept_menu/$', concept_menu_view),
    url(r'^material/(\d+)/$', pdf_view), 
    url(r'^concept_submenu/(\d+)/$', concept_submenu_view),
    url(r'^quiz/(\d+)/$', quiz_view), 
    url(r'^evaluate_quiz/$', evaluate_quiz_view), 
    url(r'^performance/$', performance_view), 
    url(r'^staff_menu/$', staff_menu_view), 
    url(r'^add_concept/$', add_concept_view), 
    url(r'^delete_concept/$', delete_concept_view), 
    url(r'^add_question/$', add_question_view), 
    url(r'^edit_question/$', edit_question_view), 
    url(r'^delete_question/$', delete_question_view), 
    url(r'^concept_upload_handler/$', concept_upload_handler), 
    url(r'^feedback/$', feedback_view), 
    url(r'^feedback_handler/$', feedback_handler), 
    url(r'^question_upload_handler/$', question_upload_handler), 
    url(r'^question_deletion_handler/$', question_deletion_handler),
    url(r'^concept_deletion_handler/$', concept_deletion_handler),  
    url(r'^add_stuff/$', add_stuff),

)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
