

def gerencia_gc(user):

    return user.groups.filter(name='gerencia_gc').count()
