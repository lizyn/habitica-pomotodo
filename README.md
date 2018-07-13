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

## drawbacks

1. can't score repeating tasks automatically due to pomotodo limitations[^1]
2. requires a local file to store id data
3. really, really slooooow
4. limited functions, hard to use [^2]
5. ...

[^1]: For the same (repeating) todo in pomotodo, its id returned through api varies each time when completed
[^2]: Actually, I write this only for my self…