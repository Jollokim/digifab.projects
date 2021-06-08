import databases.user_database as base


print(base.addUser("Jollokim", "asdqwe", 123))

print(base.getUserWithUsername("Jollokim"))
print(base.getAllUsers())

print(base.getUserWithLogin("Jollokim", "12345"))

