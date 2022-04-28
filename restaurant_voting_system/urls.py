from restaurant_voting_system import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def include_doc_api_urlpatterns():
    return [
            path('user/v1/', include('user.api.v1.urls')),
            path('voting/v1/', include('voting.api.v1.urls')),
        ]


def api_urlpatterns(namespace='api'):
    return (
        include_doc_api_urlpatterns(), namespace
    )


schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant Voting System API",
      default_version='v1',
      description="API Documentation for Restaurant Voting System."
   ),
   public=True,
   permission_classes=(),
   patterns=include_doc_api_urlpatterns(),
)


urlpatterns = [
    path('', include(api_urlpatterns())),
    path('admin/', admin.site.urls),
    path(
        'docs/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]


if settings.env.str('ENV_TYPE') == 'DEVELOPMENT':
    import debug_toolbar

    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

elif settings.env.str('ENV_TYPE') == 'STAGING':
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
