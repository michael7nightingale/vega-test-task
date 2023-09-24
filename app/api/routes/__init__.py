from . import users, watches, tasks, objects


routers = [
    users.router,
    watches.router,
    tasks.router,
    objects.router,

]
