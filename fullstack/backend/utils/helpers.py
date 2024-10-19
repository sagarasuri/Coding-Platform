def check_user_exists(users_data,new_user):
    for user in users_data:
        print(user,'welccome to Flask')
        if user.email==new_user.email and user.password==new_user.password:
            return True
    return False