from django.contrib import admin

from voting.models import Restaurant, Menu, Result, Vote


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'name',
        'address',
        'contact_no',
        'winning_streak'
    ]
    raw_id_fields = ['owner']
    search_fields = (
        'name',
        'owner__username',
        'owner__first_name',
        'owner__last_name'
    )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant',
        'menu_image',
        'num_of_votes',
        'upload_date'
    ]
    fieldsets = [
        [None, {
            'fields': [
                'restaurant',
                'menu_image',
                'num_of_votes',
                'upload_date'
            ]
        }],
    ]
    raw_id_fields = ['restaurant']
    search_fields = (
        'restaurant__name',
        'upload_date'
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = [
        'menu',
        'employee',
        'voting_date'
    ]
    raw_id_fields = [
        'menu',
        'employee'
    ]
    search_fields = (
        'menu__restaurant__name',
        'voting_date',
        'employee__username',
        'employee__first_name',
        'employee__last_name'
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        'winning_menu',
        'voting_date',
        'is_voting_stopped'
    ]
    raw_id_fields = [
        'winning_menu'
    ]
    search_fields = (
        'winning_menu__restaurant__name',
        'voting_date'
    )
    list_filter = ['is_voting_stopped']
