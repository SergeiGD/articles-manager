def create_reviewer_notification(article):
    return f'Вас назначили рецензентом на статью <a href="{article.get_show_url()}">{article.name}</a>'