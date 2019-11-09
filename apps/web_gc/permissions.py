

def user_patrimonio(user):

    return user.groups.filter(name='patrimonio').count()


def combustivel_gerencia_talao(user):

    return user.groups.filter(name='combustivel_gerencia_talao').count()


def combustivel_gerencia_vale(user):

    return user.groups.filter(name='combustivel_gerencia_vale').count()


def combustivel_beneficiario(user):

    return user.groups.filter(name='combustivel_beneficiario').count()
