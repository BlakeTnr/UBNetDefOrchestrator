from mattermostdriver import Driver

foo = Driver({
    'url': 'chat.ubnetdef.org',
    'login_id': 'EMAILHERE',
    'password': 'PASSWORDHERE',
    'scheme': 'https',
    'port': 443,
    'basepath': '/api/v4',
    'verify': False
})

foo.login()

test= foo.users.get_user(user_id='me')

jay = foo.users.get_user_by_username('jaydensh')

teams = foo.teams.get_team_by_name("UBNetDef") # mx69rrsampf6dgapamukm4w5by



# print(jay)

print(teams)

# foo.posts.create_post(options={
#     'channel_id': '6g7d4q6d9fyg3y95qrkmzkd98c',
#     'message': 'Test syssec password automated message'
# })

# print(test)