
def auth_user(token):
    pass

def get_auth_token(userid):
    user = UserProfile.objects.get(pk=userid)

    token, created = AuthToken.objects.get_or_create(user=user)
    print(token)
    if created:
        return token.token
    else:
        if token.expire > timezone.now():
            token.delete()
            new_token = AuthToken.objects.create(user=user)
            return new_token.token
        else:
            return token.token
