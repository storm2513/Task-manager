import argparse
import datetime
import sys
import dateparser
import humanize
from cli.user import UserStorage, UserInstance as User
from cli.user_session import UserSession
import cli.config as config
from tmlib import commands
import tmlib.controllers.categories_controller
import tmlib.controllers.notifications_controller
import tmlib.controllers.tasks_controller
import tmlib.controllers.task_plans_controller
from tmlib.models.category import Category
from tmlib.models.task import Task, Status, Priority
from tmlib.models.task_plan import TaskPlan
from tmlib.models.notification import Notification, Status as NotificationStatus
from tmlib.exceptions.exceptions import UserHasNoRightError


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        print('error: %s\n' % message, file=sys.stderr)
        self.print_help()
        sys.exit(2)


def init_parser():
    parser = DefaultHelpParser(
        description='Simple console task manager',
        usage='''task_manager <object> [<args>]''')
    subparser = parser.add_subparsers(
        dest='object',
        title='Commands',
        description='Choose object you want to work with',
        metavar='')

    user = subparser.add_parser(
        'user',
        help='Manage users',
        usage='task_manager user ')
    user_parser = user.add_subparsers(
        dest='action',
        title='Manage users',
        description='Commands to work with users',
        metavar='')
    create_user_parser(user_parser)

    category = subparser.add_parser(
        'category',
        help='Manage categories',
        usage='task_manager category ')
    category_parser = category.add_subparsers(
        dest='action',
        title='Manage categories',
        description='Commands to work with categories',
        metavar='')
    create_category_parser(category_parser)

    task = subparser.add_parser(
        'task',
        help='Manage tasks',
        usage='task_manager task ')
    task_parser = task.add_subparsers(
        dest='action',
        title='Manage tasks',
        description='Commands to work with tasks',
        metavar='')
    create_task_parser(task_parser)

    task_plan = subparser.add_parser(
        'plan',
        help='Manage task plans',
        usage='task_manager plan ')
    task_plan_parser = task_plan.add_subparsers(
        dest='action',
        title='Manage task plans',
        description='Commands to work with task plans',
        metavar='')
    create_task_plan_parser(task_plan_parser)

    notification = subparser.add_parser(
        'notification',
        help='Manage notifications',
        usage='task_manager notification ')
    notification_parser = notification.add_subparsers(
        dest='action',
        title='Manage notifications',
        description='Commands to work with notifications',
        metavar='')
    create_notification_parser(notification_parser)

    return parser


def create_user_parser(parser):
    parser.add_parser('add', help='Adds new user').add_argument(
        'username')

    parser.add_parser(
        'login',
        help='Authorizes user by username').add_argument('username')

    parser.add_parser('logout', help='Logouts user')
    parser.add_parser('current', help='Shows current user')
    parser.add_parser('all', help='Shows all users')


def create_category_parser(parser):
    parser.add_parser('add', help='Adds new category').add_argument(
        'name', help="category's name")

    parser.add_parser(
        'show', help='Shows category by ID').add_argument(
        'id', help="category's ID")

    update_category_parser = parser.add_parser(
        'edit', help='Edits category by ID')
    update_category_parser.add_argument(
        '-id', '--id', help="category's ID", required=True)
    update_category_parser.add_argument(
        '-n', '--name', help="category's name", required=True)

    parser.add_parser(
        'delete', help='Deletes category by ID').add_argument(
        'id', help="category's ID")

    parser.add_parser('all', help='Shows all categories')


def create_task_parser(parser):
    add_task_parser = parser.add_parser('add', help='Adds new task')
    required_add_task_arguments = add_task_parser.add_argument_group(
        'required arguments')
    optional_add_task_arguments = add_task_parser.add_argument_group(
        'optional arguments')
    required_add_task_arguments.add_argument(
        '-t', '--title', help="task's title", required=True)
    optional_add_task_arguments.add_argument(
        '-n', '--note', help="task's note")
    optional_add_task_arguments.add_argument(
        '-st', '--start_time', help="task's start time")
    optional_add_task_arguments.add_argument(
        '-et', '--end_time', help="task's end time")
    optional_add_task_arguments.add_argument(
        '-e', '--is_event', help="is task event", choices=['yes', 'no'])
    optional_add_task_arguments.add_argument(
        '-c', '--category_id', help="task's category_id")
    optional_add_task_arguments.add_argument(
        '-p',
        '--priority',
        choices=Priority.__members__,
        help="task's priority")
    optional_add_task_arguments.add_argument(
        '-r',
        '--repeat',
        help="Creates repeated task according to interval. E.g. --repeat 'every 1 week'")
    optional_add_task_arguments.add_argument(
        '-sa',
        '--start_repeat_at',
        help="Start date time for repeated task. E.g. --sa 'in 3 days'")

    edit_task_parser = parser.add_parser('edit', help='Edits task')
    required_edit_task_arguments = edit_task_parser.add_argument_group(
        'required arguments')
    optional_edit_task_arguments = edit_task_parser.add_argument_group(
        'optional arguments')
    required_edit_task_arguments.add_argument(
        '-id', '--id', help="task's ID")
    optional_edit_task_arguments.add_argument(
        '-t', '--title', help="task's title")
    optional_edit_task_arguments.add_argument(
        '-n', '--note', help="task's note")
    optional_edit_task_arguments.add_argument(
        '-st', '--start_time', help="task's start time")
    optional_edit_task_arguments.add_argument(
        '-et', '--end_time', help="task's end time")
    optional_edit_task_arguments.add_argument(
        '-e', '--is_event', help="is task event", choices=['yes', 'no'])
    optional_edit_task_arguments.add_argument(
        '-c', '--category_id', help="task's category_id")
    optional_edit_task_arguments.add_argument(
        '-p',
        '--priority',
        choices=Priority.__members__,
        help="task's priority")

    show_task_parser = parser.add_parser('show', help='Shows tasks')
    show_task_subparser = show_task_parser.add_subparsers(
        dest='show_action',
        title='Shows tasks',
        description='Commands to show tasks',
        metavar='')
    create_show_task_parser(show_task_subparser)

    parser.add_parser('delete', help='Deletes task by ID').add_argument(
        'id', help="task's ID")

    set_status_parser = parser.add_parser(
        'set_status', help='Sets status to task')
    set_status_subparser = set_status_parser.add_subparsers(
        dest='set_status_action',
        title='Set status',
        description='Sets status to task',
        metavar='')
    set_status_subparser.add_parser(
        'todo', help='Sets task as TODO by ID').add_argument(
        'id', help="task's ID")
    set_status_subparser.add_parser(
        'in_progress',
        help='Sets task as IN_PROGRESS by ID').add_argument(
        'id',
        help="task's ID")
    set_status_subparser.add_parser(
        'done', help='Sets task as DONE by ID').add_argument(
        'id', help="task's ID")
    set_status_subparser.add_parser(
        'archived', help='Sets task as ARCHIVED by ID').add_argument(
        'id', help="task's ID")

    create_inner_task_parser = parser.add_parser(
        'add_inner', help="Adds inner task by parent task's ID")
    required_create_inner_task_arguments = create_inner_task_parser.add_argument_group(
        'required arguments')
    optional_create_inner_task_arguments = create_inner_task_parser.add_argument_group(
        'optional arguments')

    required_create_inner_task_arguments.add_argument(
        '-pid', '--parent_task_id', help="parent task's ID", required=True)
    required_create_inner_task_arguments.add_argument(
        '-t', '--title', help="task's title", required=True)
    optional_create_inner_task_arguments.add_argument(
        '-n', '--note', help="task's note")
    optional_create_inner_task_arguments.add_argument(
        '-st', '--start_time', help="task's start time")
    optional_create_inner_task_arguments.add_argument(
        '-et', '--end_time', help="task's end time")
    optional_create_inner_task_arguments.add_argument(
        '-e', '--is_event', help="is task event", choices=['yes', 'no'])
    optional_create_inner_task_arguments.add_argument(
        '-c', '--category_id', help="task's category_id")
    optional_create_inner_task_arguments.add_argument(
        '-p',
        '--priority',
        choices=Priority.__members__,
        help="task's priority")

    assign_task_parser = parser.add_parser(
        'assign', help="Assigns task on user")
    assign_task_parser.add_argument(
        '-tid',
        '--task_id',
        help="assigned task's ID",
        required=True)
    assign_task_parser.add_argument(
        '-uid',
        '--user_id',
        help="user's ID",
        required=True)

    rights_parser = parser.add_parser('rights', help="Manages user's rights")
    rights_subparser = rights_parser.add_subparsers(
        dest='rights_action',
        title='Manages rights',
        description='Commands to manage rights',
        metavar='')
    create_rights_parser(rights_subparser)


def create_show_task_parser(parser):
    parser.add_parser(
        'id',
        help='Shows task by id',
        usage='task_manager task show id ').add_argument(
        'id',
        help="task's ID")

    parser.add_parser('all', help="Shows all user's tasks")

    show_inner_tasks_parser = parser.add_parser(
        'inner', help="Shows inner tasks by parent task's ID")
    show_inner_tasks_parser.add_argument('pid', help="parent task's ID")

    parser.add_parser(
        'parent',
        help="Shows parent task by inner task's ID").add_argument(
        'id',
        help="inner task's ID")

    parser.add_parser('assigned', help="Shows tasks assigned on current user")

    parser.add_parser('todo', help="Shows user's todo tasks")
    parser.add_parser('in_progress', help="Shows user's in progress tasks")
    parser.add_parser('done', help="Shows user's done tasks")
    parser.add_parser('archived', help="Shows user's archived tasks")

    parser.add_parser(
        'can_read',
        help="Shows tasks that current user can read")

    parser.add_parser(
        'can_write',
        help="Shows tasks that current user can read and write")


def create_task_plan_parser(parser):
    edit_task_plan_parser = parser.add_parser('edit', help='Edits task plan')
    edit_task_plan_parser.add_argument('id', help="Plan's ID")
    edit_task_plan_parser.add_argument(
        '-r',
        '--repeat',
        help="Creates repeated task according to interval. E.g. --repeat 'every 1 week'")
    edit_task_plan_parser.add_argument(
        '-sa',
        '--start_repeat_at',
        help="Start date time for repeated task. E.g. --sa 'in 3 days'")

    parser.add_parser('all', help='Shows all plans')


def create_rights_parser(parser):
    add_right_parser = parser.add_parser(
        'add', help='Adds right', usage='task_manager task rights add ')
    add_right_subparser = add_right_parser.add_subparsers(
        dest='rights_add_action',
        title='Adds rights',
        description='Commands to add read or write rights',
        metavar='')

    add_user_for_read_parser = add_right_subparser.add_parser(
        'read', help='Gives user right for read task')
    add_user_for_read_parser.add_argument(
        '-tid', '--task_id', help="task's ID", required=True)
    add_user_for_read_parser.add_argument(
        '-uid', '--user_id', help="user's ID", required=True)

    add_user_for_write_parser = add_right_subparser.add_parser(
        'write', help='Gives user right for read and write task')
    add_user_for_write_parser.add_argument(
        '-tid', '--task_id', help="task's ID", required=True)
    add_user_for_write_parser.add_argument(
        '-uid', '--user_id', help="user's ID", required=True)

    remove_right_parser = parser.add_parser(
        'remove',
        help='Removes right',
        usage='task_manager task rights remove ')
    remove_right_subparser = remove_right_parser.add_subparsers(
        dest='rights_remove_action',
        title='Removes rights',
        description='Commands to remove read or write rights',
        metavar='')

    remove_user_for_read_parser = remove_right_subparser.add_parser(
        'read', help='Removes user right for read task')
    remove_user_for_read_parser.add_argument(
        '-tid', '--task_id', help="task's ID", required=True)
    remove_user_for_read_parser.add_argument(
        '-uid', '--user_id', help="user's ID", required=True)

    remove_user_for_write_parser = remove_right_subparser.add_parser(
        'write', help='Removes user right for read and write task')
    remove_user_for_write_parser.add_argument(
        '-tid', '--task_id', help="task's ID", required=True)
    remove_user_for_write_parser.add_argument(
        '-uid', '--user_id', help="user's ID", required=True)


def create_notification_parser(parser):
    add_notification_parser = parser.add_parser(
        'add', help='Adds notification', usage='task_manager task rights add ')

    required_add_notification_arguments = add_notification_parser.add_argument_group(
        'required arguments')
    required_add_notification_arguments.add_argument(
        '-tid', '--task_id', help="task's ID", required=True)
    required_add_notification_arguments.add_argument(
        '-t', '--title', help="notification's title")
    required_add_notification_arguments.add_argument(
        '-st', '--relative_start_time', help="notification's relative start time")

    edit_notification_parser = parser.add_parser(
        'edit', help='Edits notification')
    required_edit_notification_arguments = edit_notification_parser.add_argument_group(
        'required arguments')
    optional_edit_notification_arguments = edit_notification_parser.add_argument_group(
        'optional arguments')
    required_edit_notification_arguments.add_argument(
        '-id', '--id', help="notification's ID")
    optional_edit_notification_arguments.add_argument(
        '-t', '--title', help="notification's title")
    optional_edit_notification_arguments.add_argument(
        '-n', '--note', help="notification's note")
    optional_edit_notification_arguments.add_argument(
        '-st', '--relative_start_time', help="notification's relative start time")

    show_notification_parser = parser.add_parser(
        'show', help='Shows notifications')
    show_notification_subparser = show_notification_parser.add_subparsers(
        dest='show_action',
        title='Shows notifications',
        description='Commands to show notification',
        metavar='')
    create_show_notification_parser(show_notification_subparser)

    parser.add_parser(
        'delete', help='Deletes notification by ID').add_argument(
        'id', help="notification's ID")


def create_show_notification_parser(parser):
    parser.add_parser(
        'id',
        help='Shows notification by id',
        usage='task_manager notification show id ').add_argument(
        'id',
        help="notification's ID")

    parser.add_parser(
        'created',
        help="Shows user's created notifications (not shown)")
    parser.add_parser('shown', help="Shows user's shown notifications")
    parser.add_parser('all', help="Shows all user's notifications")


def check_user_authorized(user_session):
    if user_session.get_current_user() is None:
        print("You should login before this action")
        quit()


def process_object(args, user_session):
    if args.object == 'user':
        process_user_action(args, user_session)
    elif args.object == 'category':
        check_user_authorized(user_session)
        process_category_action(args, user_session.get_current_user())
    elif args.object == 'task':
        check_user_authorized(user_session)
        process_task_action(args, user_session.get_current_user())
    elif args.object == 'notification':
        check_user_authorized(user_session)
        process_notification_action(args, user_session.get_current_user())
    elif args.object == 'plan':
        check_user_authorized(user_session)
        process_task_plan_action(args, user_session.get_current_user())


def process_user_action(args, user_session):
    if args.action == 'add':
        add_user(args, user_session)
    elif args.action == 'login':
        login(args, user_session)
    elif args.action == 'logout':
        logout(user_session)
    elif args.action == 'current':
        check_user_authorized(user_session)
        show_user(user_session.get_current_user())
    elif args.action == 'all':
        show_all_users()


def process_category_action(args, user):
    if args.action == 'add':
        add_category(args, user)
    elif args.action == 'show':
        show_category(args, user)
    elif args.action == 'delete':
        delete_category(args, user)
    elif args.action == 'edit':
        update_category(args, user)
    elif args.action == 'all':
        show_all_categories(user)


def process_task_action(args, user):
    if args.action == 'add':
        add_task(args, user)
    elif args.action == 'edit':
        edit_task(args, user)
    elif args.action == 'show':
        if args.show_action == 'id':
            show_task(args, user)
        elif args.show_action == 'all':
            show_all_tasks(user)
        elif args.show_action == 'inner':
            show_inner_tasks(args, user)
        elif args.show_action == 'parent':
            show_parent_task(args, user)
        elif args.show_action == 'assigned':
            show_assigned_tasks(user)
        elif args.show_action == 'todo':
            show_to_do_tasks(user)
        elif args.show_action == 'in_progress':
            show_in_progress_tasks(user)
        elif args.show_action == 'done':
            show_done_tasks(user)
        elif args.show_action == 'archived':
            show_archived_tasks(user)
        elif args.show_action == 'can_read':
            show_can_read_tasks(user)
        elif args.show_action == 'can_write':
            show_can_write_tasks(user)
    elif args.action == 'set_status':
        if args.set_status_action == 'todo':
            set_task_as_to_do(args, user)
        elif args.set_status_action == 'in_progress':
            set_task_as_in_progress(args, user)
        elif args.set_status_action == 'done':
            set_task_as_done(args, user)
        elif args.set_status_action == 'archived':
            set_task_as_archived(args, user)
    elif args.action == 'delete':
        delete_task(args, user)
    elif args.action == 'add_inner':
        create_inner_task(args, user)
    elif args.action == 'assign':
        assign_task_on_user(args, user)
    elif args.action == 'rights':
        if args.rights_action == 'add':
            if args.rights_add_action == 'read':
                add_user_for_read(args, user)
            elif args.rights_add_action == 'write':
                add_user_for_write(args, user)
        elif args.rights_action == 'remove':
            if args.rights_remove_action == 'read':
                remove_user_for_read(args, user)
            elif args.rights_remove_action == 'write':
                remove_user_for_write(args, user)


def process_notification_action(args, user):
    if args.action == 'add':
        add_notification(args, user)
    elif args.action == 'show':
        if args.show_action == 'id':
            show_notification(args, user)
        elif args.show_action == 'all':
            show_all_notifications(user)
        elif args.show_action == 'created':
            show_created_notifications(user)
        elif args.show_action == 'shown':
            show_shown_notifications(user)
    elif args.action == 'edit':
        edit_notification(args, user)
    elif args.action == 'delete':
        delete_notification(args, user)


def process_task_plan_action(args, user):
    if args.action == 'edit':
        edit_task_plan(args, user)
    elif args.action == 'all':
        show_all_task_plans(user)


def add_user(args, user_session):
    user = User(username=args.username)
    if UserStorage().create(user):
        user_session.login_user(user.username)
        print('User {} registered'.format(args.username))
    else:
        print('Error. User {} already exists'.format(args.username), file=sys.stderr)


def login(args, user_session):
    if user_session.login_user(args.username) is not None:
        print('User {} logged in'.format(args.username))
    else:
        print('User {} does not exist'.format(args.username), file=sys.stderr)


def logout(user_session):
    user_session.logout_user()
    print('User logged out')


def show_user(user):
    print(
        "ID: {}, username: {}".format(user.id, user.username))


def show_all_users():
    print("Users:")
    users = UserStorage().all_users()
    for user in users:
        print(
            "ID: {}, username: {}".format(
                user.id,
                user.username))


def add_category(args, user):
    category = Category(name=args.name)
    commands.add_category(create_categories_controller(user), category)
    print('Category "{}" added'.format(args.name))


def update_category(args, user):
    category = commands.get_category_by_id(
        create_categories_controller(user), args.id)
    if category is None:
        print("There is no category with such ID")
        quit()
    category.name = args.name
    commands.update_category(create_categories_controller(user), category)
    print(
        'Category {} with ID {} was updated'.format(
            category.name,
            category.id))


def delete_category(args, user):
    commands.delete_category(create_categories_controller(user), args.id)
    print("Category was deleted")


def show_category(args, user):
    category = commands.get_category_by_id(
        create_categories_controller(user), args.id)
    print("ID: {}, name: {}".format(category.id, category.name))


def show_all_categories(user):
    print("Categories:")
    categories = commands.user_categories(create_categories_controller(user))
    for category in categories:
        print("ID: {}, name: {}".format(category.id, category.name))


def validate_time_in_task(start_time, end_time):
    if start_time is not None and end_time is not None:
        if start_time > end_time:
            print("Error: start time greater than end time", file=sys.stderr)
            quit()


def add_task(args, user):
    task = Task(title=args.title)
    if args.note is not None:
        task.note = args.note
    if args.start_time is not None:
        task.start_time = dateparser.parse(args.start_time)
    if args.end_time is not None:
        task.end_time = dateparser.parse(args.end_time)
        validate_time_in_task(task.start_time, task.end_time)
    if args.is_event is not None:
        task.is_event = args.is_event == 'yes'
    if args.category_id is not None:
        task.category_id = args.category_id
    if args.priority is not None:
        task.priority = Priority[args.priority.upper()].value
    if args.repeat is not None:
        parsed_time = dateparser.parse(args.repeat)
        if parsed_time is None:
            print("Error. Repeat time is incorrect", file=sys.stderr)
            quit()
        else:
            interval = (datetime.datetime.now() - parsed_time).total_seconds()
            last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            if interval < 300:  # 5 minutes
                print("Error. Task's interval is incorrect", file=sys.stderr)
            else:
                if args.start_repeat_at is not None:
                    start_date = dateparser.parse(args.start_repeat_at)
                    if start_date is not None:
                        time_delta = (interval -
                                      (start_date - datetime.datetime.now()).total_seconds())
                        last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=time_delta)
            task.status = Status.TEMPLATE.value
            task_id = commands.add_task(create_tasks_controller(user), task).id
            plan = TaskPlan(
                task_id=task_id,
                user_id=user.id,
                interval=interval,
                last_created_at=last_created_at)
            commands.add_task_plan(create_task_plans_controller(user), plan)
            print('Planned task added')
    else:
        commands.add_task(create_tasks_controller(user), task)
        print('Task added')


def edit_task(args, user):
    task = commands.get_task_by_id(create_tasks_controller(user), args.id)
    if task is not None:
        if args.title is not None:
            task.title = args.title
        if args.note is not None:
            task.note = args.note
        if args.start_time is not None:
            task.start_time = dateparser.parse(args.start_time)
        if args.end_time is not None:
            task.end_time = dateparser.parse(args.end_time)
            validate_time_in_task(task.start_time, task.end_time)
        if args.is_event is not None:
            task.is_event = args.is_event == 'yes'
        if args.category_id is not None:
            task.category_id = args.category_id
        if args.priority is not None:
            task.priority = Priority[args.priority.upper()].value
        commands.update_task(create_tasks_controller(user), task)
        print("Task was updated")
    else:
        print("Error. There is no task with such ID", file=sys.stderr)


def show_task(args, user):
    task = commands.get_task_by_id(create_tasks_controller(user), args.id)
    print_task(task, user)


def delete_task(args, user):
    try:
        commands.delete_task(create_tasks_controller(user), args.id)
        print('Task with id {} deleted'.format(args.id))
    except UserHasNoRightError:
        print("User has no rights for this action", file=sys.stderr)


def set_task_as_to_do(args, user):
    commands.set_task_status(
        create_tasks_controller(user),
        args.id,
        Status.TODO.value)


def set_task_as_in_progress(args, user):
    commands.set_task_status(
        create_tasks_controller(user),
        args.id,
        Status.IN_PROGRESS.value)


def set_task_as_done(args, user):
    commands.set_task_status(
        create_tasks_controller(user),
        args.id,
        Status.DONE.value)


def set_task_as_archived(args, user):
    commands.set_task_status(
        create_tasks_controller(user),
        args.id,
        Status.ARCHIVED.value)


def create_inner_task(args, user):
    task = Task(title=args.title)
    if args.note is not None:
        task.note = args.note
    if args.start_time is not None:
        task.start_time = dateparser.parse(args.start_time)
    if args.end_time is not None:
        task.end_time = dateparser.parse(args.end_time)
        validate_time_in_task(task.start_time, task.end_time)
    if args.is_event is not None:
        task.is_event = args.is_event == 'yes'
    if args.category_id is not None:
        task.category_id = args.category_id
    if args.priority is not None:
        task.priority = Priority[args.priority.upper()].value
    commands.create_inner_task(
        create_tasks_controller(user),
        args.parent_task_id,
        task)
    print("Inner task was created")


def show_inner_tasks(args, user):
    print('Inner tasks:')
    tasks = commands.get_inner_tasks(create_tasks_controller(user), args.pid)
    print_task_list(tasks, user)


def show_parent_task(args, user):
    print('Parent task:')
    task = commands.get_parent_task(create_tasks_controller(user), args.id)
    print_task(task, user)


def assign_task_on_user(args, user):
    commands.assign_task_on_user(
        tasks_controller=create_tasks_controller(user),
        task_id=args.task_id,
        user_id=args.user_id)


def add_user_for_read(args, user):
    commands.add_user_for_read(
        tasks_controller=create_tasks_controller(user),
        user_id=args.user_id,
        task_id=args.task_id)


def add_user_for_write(args, user):
    commands.add_user_for_write(
        tasks_controller=create_tasks_controller(user),
        user_id=args.user_id,
        task_id=args.task_id)


def remove_user_for_read(args, user):
    commands.remove_user_for_read(
        tasks_controller=create_tasks_controller(user),
        user_id=args.user_id,
        task_id=args.task_id)


def remove_user_for_write(args, user):
    commands.remove_user_for_write(
        tasks_controller=create_tasks_controller(user),
        user_id=args.user_id,
        task_id=args.task_id)


def show_all_tasks(user):
    print('Tasks:')
    tasks = commands.user_tasks(create_tasks_controller(user))
    print_task_list(tasks, user)


def show_assigned_tasks(user):
    print('Assigned tasks:')
    tasks = commands.assigned_tasks(create_tasks_controller(user))
    print_task_list(tasks, user)


def show_can_read_tasks(user):
    print('Can read tasks:')
    tasks = commands.can_read_tasks(create_tasks_controller(user))
    print_task_list(tasks, user)


def show_can_write_tasks(user):
    print('Can write tasks:')
    tasks = commands.can_write_tasks(create_tasks_controller(user))
    print_task_list(tasks, user)


def show_to_do_tasks(user):
    print('TODO:')
    tasks = commands.tasks_with_status(
        create_tasks_controller(user), Status.TODO.value)
    print_task_list(tasks, user)


def show_in_progress_tasks(user):
    print('IN_PROGRESS:')
    tasks = commands.tasks_with_status(
        create_tasks_controller(user), Status.IN_PROGRESS.value)
    print_task_list(tasks, user)


def show_done_tasks(user):
    print('DONE:')
    tasks = commands.tasks_with_status(
        create_tasks_controller(user), Status.DONE.value)
    print_task_list(tasks, user)


def show_archived_tasks(user):
    print('ARCHIVED:')
    tasks = commands.tasks_with_status(
        create_tasks_controller(user), Status.ARCHIVED.value)
    print_task_list(tasks, user)


def print_task(task, user):
    if task is not None:
        result = "ID: {}".format(task.id)
        if task.parent_task_id is not None:
            result += ", parent task's id: {}".format(task.parent_task_id)
        if task.assigned_user_id is not None:
            result += ", assigned user's id: {}".format(task.assigned_user_id)
        result += ", title: {}".format(task.title)
        if task.note is not "":
            result += ", note: {}".format(task.note)
        if task.start_time is not None:
            result += ", start time: {}".format(task.start_time)
        if task.end_time is not None:
            result += ", end time: {}".format(task.end_time)
        if task.category_id is None:
            result += ", category: None"
        else:
            result += ", category: {}".format(
                commands.get_category_by_id(create_categories_controller(user),
                                            task.category_id).name)
        result += ", is event: {}, priority: {}, status: {}".format(
            task.is_event, Priority(
                task.priority).name, Status(
                task.status).name)
        result += ", created at: {}, updated_at: {}".format(
            task.created_at, task.updated_at)
        print(result)


def print_task_list(task_list, user):
    if task_list is not None:
        for task in task_list:
            print_task(task, user)


def add_notification(args, user):
    task = commands.get_task_by_id(create_tasks_controller(user), args.task_id)
    parsed_time = dateparser.parse(args.relative_start_time)
    if task is not None:
        if task.start_time is not None and parsed_time is not None:
            relative_start_time = (
                datetime.datetime.now() -
                parsed_time).total_seconds()
            notification = Notification(
                task_id=task.id,
                title=args.title,
                relative_start_time=relative_start_time)
            commands.add_notification(
                create_tasks_controller(user),
                create_notifications_controller(user),
                notification)
            print("Added notification")
        else:
            print(
                "Error. Task should have start time and notification's relative start time should be correct", file=sys.stderr)
    else:
        print("Error. Task doesn't exist", file=sys.stderr)


def edit_notification(args, user):
    notification = commands.get_notification_by_id(
        create_notifications_controller(user), args.id)
    if notification is not None:
        if args.title is not None:
            notification.title = args.title
        if args.relative_start_time is not None:
            parsed_time = dateparser.parse(args.relative_start_time)
            if parsed_time is not None:
                notification.relative_start_time = (
                    datetime.datetime.now() -
                    parsed_time).total_seconds()
        commands.update_notification(
            create_tasks_controller(user),
            create_notifications_controller(user),
            notification)
        print("Updated notification")
    else:
        print("Error. There is not notification with such ID", file=sys.stderr)


def delete_notification(args, user):
    commands.delete_notification(
        create_notifications_controller(user), args.id)
    print("Notification was deleted")


def show_notification(args, user):
    notification = commands.get_notification_by_id(
        create_notifications_controller(user), args.id)
    print_notification(notification)


def show_all_notifications(user):
    notifications = commands.user_notifications(
        create_notifications_controller(user))
    print_notification_list(notifications)


def show_created_notifications(user):
    notifications = commands.user_created_notifications(
        create_notifications_controller(user))
    print_notification_list(notifications)


def show_shown_notifications(user):
    notifications = commands.user_shown_notifications(
        create_notifications_controller(user))
    print_notification_list(notifications)


def print_notification(notification):
    print(
        "ID: {}, task_id: {}, title: {}, relative_start_time: {}, status: {}".format(
            notification.id,
            notification.task_id,
            notification.title,
            humanize.naturaldelta(
                datetime.timedelta(
                    seconds=notification.relative_start_time)),
            NotificationStatus(
                notification.status).name))


def print_notification_list(notifications):
    if notifications is not None:
        for notification in notifications:
            print_notification(notification)


def show_pending_notifications(user):
    notifications = commands.pending_notifications(
        create_notifications_controller(user))
    if notifications:
        print('Notifications')
        for notification in notifications:
            commands.set_notification_as_shown(
                create_notifications_controller(user), notification.id)
            print_notification(notification)


def edit_task_plan(args, user):
    plan = commands.get_task_plan_by_id(
        create_task_plans_controller(user), args.id)
    if plan is not None:
        if args.repeat is not None:
            parsed_time = dateparser.parse(args.repeat)
            if parsed_time is None:
                print("Error. Repeat time is incorrect", file=sys.stderr)
            else:
                interval = (
                    datetime.datetime.now() -
                    parsed_time).total_seconds()
                last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
                if interval < 300:  # 5 minutes
                    print("Error. Task's interval is incorrect", file=sys.stderr)
                else:
                    plan.interval = interval
        if args.start_repeat_at is not None:
            start_date = dateparser.parse(args.start_repeat_at)
            if start_date is not None:
                time_delta = (interval -
                              (start_date - datetime.datetime.now()).total_seconds())
                last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=time_delta)
                plan.last_created_at = last_created_at
        commands.update_task_plan(create_task_plans_controller(user), plan)
        print("Updated task plan")
    else:
        print("Error. There is no task plan with such ID", file=sys.stderr)


def show_all_task_plans(user):
    plans = commands.get_task_plans(create_task_plans_controller(user))
    print_task_plan_list(plans)


def print_task_plan(plan):
    print(
        "ID: {}, task ID: {}, interval: {}, last created at: {}".format(
            plan.id,
            plan.task_id,
            humanize.naturaldelta(
                datetime.timedelta(
                    seconds=plan.interval)),
            plan.last_created_at))


def print_task_plan_list(plans):
    if plans is not None:
        for plan in plans:
            print_task_plan(plan)


def create_tasks_controller(user, database_name=config.DATABASE):
    return tmlib.controllers.tasks_controller.create_tasks_controller(
        user.id, database_name)


def create_categories_controller(user, database_name=config.DATABASE):
    return tmlib.controllers.categories_controller.create_categories_controller(
        user.id, database_name)


def create_notifications_controller(user, database_name=config.DATABASE):
    return tmlib.controllers.notifications_controller.create_notifications_controller(
        user.id, database_name)


def create_task_plans_controller(user, database_name=config.DATABASE):
    return tmlib.controllers.task_plans_controller.create_task_plans_controller(
        user.id, database_name)


def handle_commands():
    user_session = UserSession(
        config_file=config.CONFIG_FILE,
        database_name=config.DATABASE)
    current_user = user_session.get_current_user()
    if current_user is not None:
        create_notifications_controller(current_user).process_notifications()
        create_task_plans_controller(current_user).process_plans(
            create_tasks_controller(current_user))
        show_pending_notifications(current_user)

    parser = init_parser()
    args = parser.parse_args()
    process_object(args, user_session)
