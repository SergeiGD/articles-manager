def create_reviewer_notification(article):
    return f'Вас назначили рецензентом на статью <a href="{article.get_detail_url()}">{article.name}</a>'

def create_republished_notification(article):
    return f'В статью <a href="{article.get_detail_url()}">{article.name}</a> внесены правки, требуется рецензия'

def create_voting_notification(voting):
    return f'Назначено голосование <a href="{voting.get_detail_url()}">{voting.article.name}</a>. Дата начала - {voting.date_start}'
