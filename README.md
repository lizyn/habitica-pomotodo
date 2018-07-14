## What's this

Scripts that help sync between habitodo and pomotodo (a pomodoro service)

## What can it do

1. sync new tasks in habitica to pomotodo
2. score back in habitica when related todos completed in pomotodo

### Supported

- [x] subtasks
- [x] score back in habitica
- [x] repeating tasks
- [x] filter tasks
- [ ] a shabby gui for iOS app Pythonista

### dependencies

- [dotenv (a python module)](https://github.com/theskumar/python-dotenv)

## drawbacks

1. can't score repeating tasks automatically due to pomotodo limitations <sup>[1](#fn1)</sup>
2. requires a local file to store id data
3. really, really slooooow
4. limited functions, hard to use <sup>[2](#fn1)</sup>
5. ...

## todos

- [x] port to  Pythonista on iOS
- [ ] use asyncio / aiohttp to accelerate syncing process
- [ ] better UI for Pythonista

<a name="fn1">1</a>: For the same (repeating) todo in pomotodo, its id returned through api varies each time when completed

<a name="fn2">2</a>: Actually, I write this only for my self…