# proc-python

proc-python - A Python module for retrieving information about running processes in Linux

## Documentation

* class Process(pid)
    * env -> dict
        * The environment variables of the process.
    * cmdline -> list<str>
        * The command line arguments of the process.
    * started -> datetime
        * The start time of the process.
    * name -> str
        * The name of the process. Uses the first command line argument or the `comm` file if the `cmdline` is empty. 
    * suspend(int resume_after?)
        * Suspends the process. Resumes after `resume_after` milliseconds if given.
    * resume()
        * Resumes the process after suspending.
    * kill(bool force?)
        * Kills the process. Uses `SIGKILL` instead of `SIGTERM` if `force` is enabled.

* get_processes(str process_name?)
    * Lists every running process by finding entries in `/proc` that are PIDs. If `process_name` is given, only show processes with the name `process_name`.

## Examples

```python
""" Kill every Firefox process """

# import the module
import proc

# get an iterator with every firefox process
firefoxes = proc.get_processes(process_name="firefox")

# print the process and kill it
for firefox in firefoxes:
    print(firefox) # Process(pid=7382, name='firefox')
```
