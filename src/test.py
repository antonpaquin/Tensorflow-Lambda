#! /usr/bin/python3

from classify import handle

# Here: call the "handle" method with arguments that you think will cause
# full coverage, and print the results to verify functionality

print(
    handle(
        {
            'example_event': None,
        }, 
        {
            'example_context': None,
        },
    )
)
