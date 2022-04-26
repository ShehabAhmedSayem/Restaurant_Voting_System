from voting.models import Menu, Result


def update_result(voting_date):
    result_updated = False
    result, _ = Result.objects.get_or_create(voting_date=voting_date)
    menus = (
        Menu.objects
        .filter(upload_date=voting_date)
        .select_related('restaurant')
    )
    if menus.count() > 0:
        if (
            menus[0].restaurant.winning_streak >= 3
            and menus.count() > 1
        ):
            menus[0].restaurant.reset_winning_streak()
            result.winning_menu = menus[1]
            menus[1].restaurant.increment_winning_streak()
        else:
            result.winning_menu = menus[0]
            menus[0].restaurant.increment_winning_streak()
        result.stop_voting()
        result_updated = True
    else:
        result_updated = False

    return result_updated, result
