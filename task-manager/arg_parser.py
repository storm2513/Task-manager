import argparse
from config import commands
from config.session import Global
from models.user import User
from models.category import Category
from models.task import Task
from enums.priority import Priority
from enums.status import Status


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

    update_category_parser = parser.add_parser(
        'edit', help='Edits category by ID')
    update_category_parser.add_argument(
        '-id', '--id', help="category's ID", required=True)
    update_category_parser.add_argument(
        '-n', '--name', help="category's name", required=True)

    delete_category_parser = parser.add_parser(
        'delete', help='Deletes category by ID')
    delete_category_parser.add_argument(
        '-id', '--id', help="category's ID", required=True)

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
        '-e', '--is_event', help="is task event")
    optional_add_task_arguments.add_argument(
        '-c', '--category_id', help="task's category_id")
    optional_add_task_arguments.add_argument(
        '-p', '--priority', help="task's priority")

    parser.add_parser('all', help='Shows all tasks')


def parse_object(args):
    if args.object == 'user':
        parse_user_action(args)
    elif args.object == 'category':
        parse_category_action(args)
    elif args.object == 'task':
        parse_task_action(args)


def parse_user_action(args):
    if args.action == 'add':
        add_user(args)
    elif args.action == 'login':
        login_user(args)
    elif args.action == 'logout':
        logout_user()
    elif args.action == 'current':
        current_user()
    elif args.action == 'edit':
        update_user(args)
    elif args.action == 'all':
        show_all_users()


def parse_category_action(args):
    if args.action == 'add':
        add_category(args)
    if args.action == 'delete':
        delete_category(args)
    if args.action == 'edit':
        update_category(args)
    if args.action == 'all':
        show_all_categories()


def parse_task_action(args):
    if args.action == 'add':
        add_task(args)
    if args.action == 'all':
        all_tasks()


def add_user(args):
    user = User(email=args.email, name=args.name, password=args.password)
    commands.add_user(user)


def login_user(args):
    commands.login_user(email=args.email, password=args.password)


def update_user(args):
    user = commands.current_user()
    if args.name is not None:
        user.name = args.name
    if args.password is not None:
        user.password = args.password
    commands.update_user(user)


def logout_user():
    commands.logout_user()


def current_user():
    user = commands.current_user()
    print("ID: {}, email: {}, name: {}, password: {}".format(
        user.id, user.email, user.name, user.password))


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
    category.name = args.name
    commands.update_category(category)


def delete_category(args):
    commands.delete_category(args.id)


def show_all_categories():
    print("Categories:")
    categories = commands.all_categories()
    for category in categories:
        print("ID: {}, name: {}".format(category.id, category.name))

# TODO: parse time and priority, add validations


def add_task(args):
    user_id = Global.USER.id
    task = Task(title=args.title, user_id=user_id)
    if args.note is not None:
        task.note = args.note
    if args.start_time is not None:
        task.start_time = args.start_time
    if args.end_time is not None:
        task.end_time = args.end_time
    if args.is_event is not None:
        task.is_event = args.is_event
    if args.category_id is not None:
        task.category_id = args.category_id
    if args.priority is not None:
        task.priority = args.priority
    commands.add_task(task)


def all_tasks():
    print('Tasks:')
    tasks = commands.user_tasks()
    for task in tasks:
        result = "ID: {}, title: {}".format(task.id, task.title)
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
        print(result)


def process_args():
    parser = init_parser()
    args = parser.parse_args()
    parse_object(args)
