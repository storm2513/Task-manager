import argparse
from config import commands
from config.session import Global
from models.user import User
from models.category import Category
from models.task import Task
from enums.priority import Priority
from enums.status import Status
from dateutil import parser as date_parser


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

    show_category_parser = parser.add_parser(
        'show', help='Shows category by ID')
    show_category_parser.add_argument(
        'id', help="category's ID")

    update_category_parser = parser.add_parser(
        'edit', help='Edits category by ID')
    update_category_parser.add_argument(
        '-id', '--id', help="category's ID", required=True)
    update_category_parser.add_argument(
        '-n', '--name', help="category's name", required=True)

    delete_category_parser = parser.add_parser(
        'delete', help='Deletes category by ID')
    delete_category_parser.add_argument(
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

    delete_task_parser = parser.add_parser('delete', help='Deletes task by ID')
    delete_task_parser.add_argument(
        'id', help="task's ID")

    set_task_as_to_do_parser = parser.add_parser(
        'set_as_to_do', help='Sets task as TODO by ID')
    set_task_as_to_do_parser.add_argument(
        'id', help="task's ID")

    set_task_as_in_progress_parser = parser.add_parser(
        'set_as_in_progress', help='Sets task as IN_PROGRESS by ID')
    set_task_as_in_progress_parser.add_argument(
        'id', help="task's ID")

    set_task_as_done_parser = parser.add_parser(
        'set_as_done', help='Sets task as DONE by ID')
    set_task_as_done_parser.add_argument(
        'id', help="task's ID")

    set_task_as_archived_parser = parser.add_parser(
        'set_as_archived', help='Sets task as ARCHIVED by ID')
    set_task_as_archived_parser.add_argument(
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
    id_parser = parser.add_parser(
        'id',
        help='Shows task by id',
        usage='task_manager task show id ')
    id_parser.add_argument('id', help="task's ID")

    parser.add_parser('all', help="Shows all user's tasks")

    show_inner_tasks_parser = parser.add_parser(
        'inner', help="Shows inner tasks by parent task's ID")
    show_inner_tasks_parser.add_argument('pid', help="parent task's ID")

    show_parent_task_parser = parser.add_parser(
        'parent', help="Shows parent task by inner task's ID")
    show_parent_task_parser.add_argument('id', help="inner task's ID")

    parser.add_parser('assigned', help="Shows tasks assigned on current user")

    parser.add_parser(
        'can_read',
        help="Shows tasks that current user can read")

    parser.add_parser(
        'can_write',
        help="Shows tasks that current user can read and write")


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
        elif args.show_action == 'can_read':
            show_can_read_tasks()
        elif args.show_action == 'can_write':
            show_can_write_tasks()
    elif args.action == 'set_as_to_do':
        set_task_as_to_do(args)
    elif args.action == 'set_as_in_progress':
        set_task_as_in_progress(args)
    elif args.action == 'set_as_done':
        set_task_as_done(args)
    elif args.action == 'set_as_archived':
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
        task.start_time = date_parser.parse(args.start_time)
    if args.end_time is not None:
        task.end_time = date_parser.parse(args.end_time)
        validate_time_in_task(task.start_time, task.end_time)
    if args.is_event is not None:
        task.is_event = args.is_event == 'yes'
    if args.category_id is not None:
        task.category_id = args.category_id
    if args.priority is not None:
        task.priority = Priority[args.priority.upper()].value
    commands.add_task(task)


def edit_task(args):
    task = commands.get_task_by_id(args.id)
    if args.title is not None:
        task.title = args.title
    if args.note is not None:
        task.note = args.note
    if args.start_time is not None:
        task.start_time = date_parser.parse(args.start_time)
    if args.end_time is not None:
        task.end_time = date_parser.parse(args.end_time)
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
    commands.delete_task(args.id)


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
        task.start_time = date_parser.parse(args.start_time)
    if args.end_time is not None:
        task.end_time = date_parser.parse(args.end_time)
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
        print(result)


def print_task_list(task_list):
    for task in task_list:
        print_task(task)


def process_args():
    parser = init_parser()
    args = parser.parse_args()
    parse_object(args)
