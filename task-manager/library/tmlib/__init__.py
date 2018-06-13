"""
Simple library for task management

All public methods for working with task manager are located in tmlib.commands module.

This library has 4 entities: Category, Notification, Task and TaskPlan. They are described in tmlib.models package.
To connect these entities with database, this library uses appropriate controller (CategoriesController, NotificationsController, TaskPlansController or TasksController). All controllers are described in tmlib.controllers package.
There are functions that simplify process of creating controller in each controller's module. E.g. create_tasks_controller(user_id, database_name).
To work with public methods, at least you should pass appropriate controller for entities with which you want to work. E.g. if you want to work with tasks, you should pass TasksController instance.

Creating task:

    >>> from tmlib.models.task import Task
    >>> from tmlib.controllers.tasks_controller import create_tasks_controller
    >>> task = Task(user_id=USER_ID, title="Title example", note="This is an example task")
    >>> tasks_controller = create_tasks_controller(USER_ID, '/your/database/path/database_name')
    >>> tmlib.commands.add_task(tasks_controller, task)

Creating inner task:

    >>> from tmlib.controllers.tasks_controller import create_tasks_controller
    >>> from tmlib.models.task import Task
    >>> inner_task = Task(user_id=USER_ID, title="Inner task", note="This task will belong to task with id == PARENT_TASK_ID")
    >>> tasks_controller = create_tasks_controller(USER_ID, '/your/database/path/database_name')
    >>> tmlib.commands.create_inner_task(tasks_controller, PARENT_TASK_ID, inner_task)

Getting all user's tasks:

    >>> from tmlib.controllers.tasks_controller import create_tasks_controller
    >>> tasks_controller = create_tasks_controller(USER_ID, '/your/database/path/database_name')
    >>> tasks_list = tmlib.commands.user_tasks(tasks_controller)
"""