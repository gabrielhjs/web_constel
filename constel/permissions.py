

def gerencia_gc(user):

    return user.groups.filter(name='gerencia_gc').count()


def gerencia_cont(user):

    return user.groups.filter(name='gerencia_cont').count()

