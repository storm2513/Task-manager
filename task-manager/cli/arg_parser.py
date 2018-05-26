import argparse
from config import commands
from config.session import Global
from models.user import User
from models.category import Category
from models.task import Task
from models.task_plan import TaskPlan
from models.notification import Notification
from enums.priority import Priority
from enums.status import Status
from enums.notification_status import NotificationStatus
import datetime
import dateparser
import humanize
from exceptions.exceptions import *


def init_parser():
    parser = argparse.ArgumentParser(
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

    logging = subparser.add_parser(
        'logging',
        help='Manage logging',
        usage='task_manager logging ')
    logging.add_argument('enabled', choices=['on', 'off'], help='Enables or disables logging')

    return parser


def create_user_parser(parser):
    add_user_parser = parser.add_parser('add', help='Adds new user')
    required_add_user_arguments = add_user_parser.add_argument_group(
        'required arguments')
    required_add_user_arguments.add_argument(
        '-e', '--email', help="user's email", required=True)
    required_add_user_arguments.add_argument(
        '-n', '--name', help="user's name", required=True)
    required_add_user_arguments.add_argument(
        '-p', '--password', help="user's password", required=True)

    login_user_parser = parser.add_parser(
        'login', help='Authorizes user by email and password')
    required_login_user_arguments = login_user_parser.add_argument_group(
        'required arguments')
    required_login_user_arguments.add_argument(
        '-e', '--email', help="user's email", required=True)
    required_login_user_arguments.add_argument(
        '-p', '--password', help="user's password", required=True)

    update_user_parser = parser.add_parser(
        'edit', help="Edits user's name and password")
    update_user_parser.add_argument('-n', '--name', help="user's name")
    update_user_parser.add_argument('-p', '--password', help="user's password")

    parser.add_parser('logout', help='Logouts user')
    parser.add_parser('current', help='Shows current user')
    parser.add_parser('all', help='Shows all users')


def create_category_parser(parser):
    add_category_parser = parser.add_parser('add', help='Adds new category')
    add_category_parser.add_argument(
        '-n', '--name', help="category's name", required=True)

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


def check_user_authorized():
    if Global.USER is None:
        print("You should login before this action")
        quit()


def parse_object(args):
    if args.object == 'user':
        parse_user_action(args)
    elif args.object == 'category':
        check_user_authorized()
        parse_category_action(args)
    elif args.object == 'task':
        check_user_authorized()
        parse_task_action(args)
    elif args.object == 'notification':
        check_user_authorized()
        parse_notification_action(args)
    elif args.object == 'plan':
        check_user_authorized()
        parse_task_plan_action(args)
    elif args.object == 'logging':
        change_logging_level(args)


def parse_user_action(args):
    if args.action == 'add':
        add_user(args)
    elif args.action == 'login':
        login_user(args)
    elif args.action == 'logout':
        logout_user()
    elif args.action == 'current':
        check_user_authorized()
        current_user()
    elif args.action == 'edit':
        check_user_authorized()
        update_user(args)
    elif args.action == 'all':
        show_all_users()


def parse_category_action(args):
    if args.action == 'add':
        add_category(args)
    elif args.action == 'show':
        show_category(args)
    elif args.action == 'delete':
        delete_category(args)
    elif args.action == 'edit':
        update_category(args)
    elif args.action == 'all':
        show_all_categories()


def parse_task_action(args):
    if args.action == 'add':
        add_task(args)
    elif args.action == 'edit':
        edit_task(args)
    elif args.action == 'show':
        if args.show_action == 'id':
            show_task(args)
        elif args.show_action == 'all':
            show_all_tasks()
        elif args.show_action == 'inner':
            show_inner_tasks(args)
        elif args.show_action == 'parent':
            show_parent_task(args)
        elif args.show_action == 'assigned':
            show_assigned_tasks()
        elif args.show_action == 'todo':
            show_to_do_tasks()
        elif args.show_action == 'in_progress':
            show_in_progress_tasks()
        elif args.show_action == 'done':
            show_done_tasks()
        elif args.show_action == 'archived':
            show_archived_tasks()
        elif args.show_action == 'can_read':
            show_can_read_tasks()
        elif args.show_action == 'can_write':
            show_can_write_tasks()
    elif args.action == 'set_status':
        if args.set_status_action == 'todo':
            set_task_as_to_do(args)
        elif args.set_status_action == 'in_progress':
            set_task_as_in_progress(args)
        elif args.set_status_action == 'done':
            set_task_as_done(args)
        elif args.set_status_action == 'archived':
            set_task_as_archived(args)
    elif args.action == 'delete':
        delete_task(args)
    elif args.action == 'add_inner':
        create_inner_task(args)
    elif args.action == 'assign':
        assign_task_on_user(args)
    elif args.action == 'rights':
        if args.rights_action == 'add':
            if args.rights_add_action == 'read':
                add_user_for_read(args)
            elif args.rights_add_action == 'write':
                add_user_for_write(args)
        elif args.rights_action == 'remove':
            if args.rights_remove_action == 'read':
                remove_user_for_read(args)
            elif args.rights_remove_action == 'write':
                remove_user_for_write(args)


def parse_notification_action(args):
    if args.action == 'add':
        add_notification(args)
    elif args.action == 'show':
        if args.show_action == 'id':
            show_notification(args)
        elif args.show_action == 'all':
            show_all_notifications()
        elif args.show_action == 'created':
            show_created_notifications()
        elif args.show_action == 'shown':
            show_shown_notifications()
    elif args.action == 'edit':
        edit_notification(args)
    elif args.action == 'delete':
        delete_notification(args)


def parse_task_plan_action(args):
    if args.action == 'edit':
        edit_task_plan(args)
    elif args.action == 'all':
        show_all_task_plans()


def add_user(args):
    user = User(email=args.email, name=args.name, password=args.password)
    try:
        commands.add_user(user)
    except InvalidEmailError as e:
        print('Error. Email "{}" is invalid'.format(e.email))
    except UserAlreadyExistsError as e:
        print('Error. User with email {} already exists'.format(e.email))


def login_user(args):
    try:
        commands.login_user(email=args.email, password=args.password)
        print('User {} logged in'.format(args.email))
    except IncorrectPasswordError as e:
        print('Password "{}" is incorrect'.format(args.password))
    except UserDoesNotExistError as e:
        print('User does not exist')


def update_user(args):
    user = commands.current_user()
    if args.name is not None:
        user.name = args.name
    if args.password is not None:
        user.password = args.password
    commands.update_user(user)
    print('User updated')


def logout_user():
    commands.logout_user()
    print('User logged out')


def current_user():
    user = commands.current_user()
    level = commands.get_level_by_user_id(user.id)
    print(
        "ID: {}, email: {}, name: {}, password: {}, level: {}, remained experience for next level: {}".format(
            user.id,
            user.email,
            user.name,
            user.password,
            level.current_level(),
            level.next_level_experience() -
            level.experience))


def show_all_users():
    print("Users:")
    users = commands.all_users()
    for user in users:
        print(
            "ID: {}, email: {}, name: {}".format(
                user.id,
                user.email,
                user.name))


def add_category(args):
    category = Category(name=args.name)
    commands.add_category(category)


def update_category(args):
    category = commands.get_category_by_id(args.id)
    if category is None:
        print("There is no category with such ID")
        quit()
    category.name = args.name
    commands.update_category(category)


def delete_category(args):
    commands.delete_category(args.id)


def show_category(args):
    category = commands.get_category_by_id(args.id)
    print("ID: {}, name: {}".format(category.id, category.name))


def show_all_categories():
    print("Categories:")
    categories = commands.all_categories()
    for category in categories:
        print("ID: {}, name: {}".format(category.id, category.name))


def validate_time_in_task(start_time, end_time):
    if start_time is not None and end_time is not None:
        if start_time > end_time:
            print("Error: start time greater than end time")
            quit()


def add_task(args):
    user_id = Global.USER.id
    task = Task(title=args.title, user_id=user_id)
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
            print("Repeat time is incorrect")
            quit()
        else:
            interval = (datetime.datetime.now() - parsed_time).total_seconds()
            last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            if interval < 300:  # 5 minutes
                print("task's interval is incorrect")
            else:
                if args.start_repeat_at is not None:
                    start_date = dateparser.parse(args.start_repeat_at)
                    if start_date is not None:
                        time_delta = interval - \
                            (start_date - datetime.datetime.now()).total_seconds()
                        last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=time_delta)
            task.status = Status.TEMPLATE.value
            task_id = commands.add_task(task).id
            plan = TaskPlan(
                task_id=task_id,
                user_id=Global.USER.id,
                interval=interval,
                last_created_at=last_created_at)
            commands.add_task_plan(plan)
            print('Planned task added')
    else:
        commands.add_task(task)
        print('Task added')


def edit_task(args):
    task = commands.get_task_by_id(args.id)
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
    commands.update_task(task)


def show_task(args):
    task = commands.get_task_by_id(args.id)
    print_task(task)


def delete_task(args):
    try:
        commands.delete_task(args.id)
        print('Task with id {} deleted'.format(args.id))
    except:
        print("User has no rights for this action")


def set_task_as_to_do(args):
    commands.set_task_as_to_do(args.id)


def set_task_as_in_progress(args):
    commands.set_task_as_in_progress(args.id)


def set_task_as_done(args):
    commands.set_task_as_done(args.id)


def set_task_as_archived(args):
    commands.set_task_as_archived(args.id)


def create_inner_task(args):
    user_id = Global.USER.id
    task = Task(title=args.title, user_id=user_id)
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
    commands.create_inner_task(args.parent_task_id, task)


def show_inner_tasks(args):
    print('Inner tasks:')
    tasks = commands.get_inner_tasks(args.pid)
    print_task_list(tasks)


def show_parent_task(args):
    print('Parent task:')
    task = commands.get_parent_task(args.id)
    print_task(task)


def assign_task_on_user(args):
    commands.assign_task_on_user(task_id=args.task_id, user_id=args.user_id)


def add_user_for_read(args):
    commands.add_user_for_read(user_id=args.user_id, task_id=args.task_id)


def add_user_for_write(args):
    commands.add_user_for_write(user_id=args.user_id, task_id=args.task_id)


def remove_user_for_read(args):
    commands.remove_user_for_read(user_id=args.user_id, task_id=args.task_id)


def remove_user_for_write(args):
    commands.remove_user_for_write(user_id=args.user_id, task_id=args.task_id)


def show_all_tasks():
    print('Tasks:')
    tasks = commands.user_tasks()
    print_task_list(tasks)


def show_assigned_tasks():
    print('Assigned tasks:')
    tasks = commands.assigned_tasks()
    print_task_list(tasks)


def show_can_read_tasks():
    print('Can read tasks:')
    tasks = commands.can_read_tasks()
    print_task_list(tasks)


def show_can_write_tasks():
    print('Can write tasks:')
    tasks = commands.can_write_tasks()
    print_task_list(tasks)


def show_to_do_tasks():
    print('TODO:')
    tasks = commands.tasks_with_status(Status.TODO.value)
    print_task_list(tasks)


def show_in_progress_tasks():
    print('IN_PROGRESS:')
    tasks = commands.tasks_with_status(Status.IN_PROGRESS.value)
    print_task_list(tasks)


def show_done_tasks():
    print('DONE:')
    tasks = commands.tasks_with_status(Status.DONE.value)
    print_task_list(tasks)


def show_archived_tasks():
    print('ARCHIVED:')
    tasks = commands.tasks_with_status(Status.ARCHIVED.value)
    print_task_list(tasks)


def print_task(task):
    if task is not None:
        result = "ID: {}".format(task.id)
        if task.parent_task_id is not None:
            result += ", parent task's id: {}".format(task.parent_task_id)
        if task.assigned_user_id is not None:
            result += ", assigned to user: {}".format(
                commands.get_user_email_by_id(task.assigned_user_id))
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
                commands.get_category_by_id(
                    task.category_id).name)
        result += ", is event: {}, priority: {}, status: {}".format(
            task.is_event, Priority(
                task.priority).name, Status(
                task.status).name)
        result += ", created at: {}, updated_at: {}".format(
            task.created_at, task.updated_at)
        print(result)


def print_task_list(task_list):
    if task_list is not None:
        for task in task_list:
            print_task(task)


def add_notification(args):
    task = commands.get_task_by_id(args.task_id)
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
            commands.add_notification(notification)
        else:
            print(
                "Task should have start time and notification's relative start time should be correct")
    else:
        print("Task doesn't exist")


def edit_notification(args):
    notification = commands.get_notification_by_id(args.id)
    if args.title is not None:
        notification.title = args.title
    parsed_time = dateparser.parse(args.relative_start_time)
    if parsed_time is not None:
        notification.relative_start_time = (
            datetime.datetime.now() -
            parsed_time).total_seconds()
    commands.update_notification(notification)


def delete_notification(args):
    commands.delete_notification(args.id)


def show_notification(args):
    notification = commands.get_notification_by_id(args.id)
    print_notification(notification)


def show_all_notifications():
    notifications = commands.user_notifications()
    print_notification_list(notifications)


def show_created_notifications():
    notifications = commands.user_created_notifications()
    print_notification_list(notifications)


def show_shown_notifications():
    notifications = commands.user_shown_notifications()
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


def show_pending_notifications():
    check_user_authorized()
    notifications = commands.pending_notifications()
    if notifications:
        print('Notifications')
        for notification in notifications:
            commands.set_notification_as_shown(notification.id)
            print_notification(notification)


def edit_task_plan(args):
    plan = commands.get_task_plan_by_id(args.id)
    if args.repeat is not None:
        parsed_time = dateparser.parse(args.repeat)
        if parsed_time is None:
            print("Repeat time is incorrect")
        else:
            interval = (datetime.datetime.now() - parsed_time).total_seconds()
            last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            if interval < 300:  # 5 minutes
                print("task's interval is incorrect")
            else:
                plan.interval = interval
    if args.start_repeat_at is not None:
        start_date = dateparser.parse(args.start_repeat_at)
        if start_date is not None:
            time_delta = interval - \
                (start_date - datetime.datetime.now()).total_seconds()
            last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=time_delta)
            plan.last_created_at = last_created_at
    commands.update_task_plan(plan)


def show_all_task_plans():
    plans = commands.get_task_plans()
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


def change_logging_level(args):
    if args.enabled == 'on':
        commands.enable_logging(True)
        print('Logging enabled')
    elif args.enabled == 'off':
        commands.enable_logging(False)
        print('Logging disabled')


def process_args():
    if Global.USER is not None:
        show_pending_notifications()
    parser = init_parser()
    args = parser.parse_args()
    parse_object(args)
