# Task Manager. Library and Console version. #

## What is it? ##

It's a simple task manager. It allows you to create and edit tasks, track their progress, assign categories to tasks, set dedlines, create notifications for important tasks and events, create inner tasks! Moreover you can work together with your friends and colleagues: just assign task on someone or give read/write access for task!

If you don't like how this console application looks and feels, you can create your own by using task manager library.

## How to install? ##

### Make sure you have installed setuptools: ###

```bash
$ pip3 install -U pip setuptools 
```

### Installing Library: ###

```bash
$ cd library
$ python3 setup.py install
```

### Running tests: ###
```bash
$ python3 setup.py test
```

### Installing Console version: ###
```bash
$ cd console
$ python3 setup.py install
```

## How to use? ##

### Working with tasks ###
```bash
$ task-manager task
```

### Working with users ###
```bash
$ task-manager user
```

### Working with tasks' categories ###
```bash
$ task-manager category
```

### Working with task plans ###
```bash
$ task-manager plan
```

### Working with notifications ###
```bash
$ task-manager notification
```

### For documentation add '-h' ###


### Configuring library logging: ###
```python
from tmlib.logger import setup_lib_logging

setup_lib_logging(
	enabled=True,
	log_all_levels=True,
	log_file_path='/path/to/log/file',
	log_format='%(asctime)s, %(name)s, [%(levelname)s]: %(message)s')
```

Made by Maksim Shylov.
