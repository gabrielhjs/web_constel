from django.contrib.auth.decorators import user_passes_test


def permission(*group_names):
    """
    Requires user membership in at least one of the groups passed in.
    """

    def in_groups(user):

        if user.is_authenticated:

            for group in group_names:

                if not bool(user.groups.filter(name=group)):

                    return False

        return True

    return user_passes_test(in_groups, login_url='/acesso-restrito/', redirect_field_name=None)
