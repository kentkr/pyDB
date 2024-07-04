pyDB, a simple project with a simple goal: learn how databases work.

At the core of data engineering lives databases and distributed systems. Two immensley
complex topics. As a foray into them, I'm iteratively building my own simple database,
taking courses, and adding complexity as I go. 

# Phase 1 - hello world

The first version will help me learn the basics, with no tutorials, all written 
in python. It'll include:
- A command line interface
    - REPL with pretty printing
    - command history
- A tokenizer with `create table` and `select` commands
- A CSV serializer/deserializer
- Unit and integration tests
- Error handling
- Logging

# Phase 2 - optimization

The next step will include taking a [CMU course](https://www.youtube.com/watch?v=vdPALZ-GCfI&list=PLSE8ODhjZXjbj8BMuIrRcacnQh20hmY9g&ab_channel=CMUDatabaseGroup) 
on databases. The optimizations are TBD based on what I learn. They may include
- Storage updates for
    - compression
    - data versioning
    - distributed storage 
- Query optimizers
- More advanced commands like
    - Aggregate functions
    - Where clauses

# Phase 3 - rustify

Python is not the optimal language for a database. So pyDB will either be rewritten
in rust or C++. That's it!

# Phase 4 - conquer the world?

By conquer the world I mean help others. Obviously. I hope to contribute to some
popular opensource databases. Ideally ones that solve a common issue like 
distributed compute or in-memory processing.
