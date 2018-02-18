# Lab 14

## Dump existing data

### MySQL

1. Create then/or select the target database

* Create: `CREATE database database_name` then `Use database_name`.
* Select: `Use database_name`

2. Dump the resource

    ```SQL
    source dump_source.sql
    ```

Done!

> This needs to be done in the same directory with the dump_source.

### MongoDB


1. Dump the resource in the shell instead of in mongodb

    ```
    mongorestore
    ```

Done!

> This needs to be done in the same directory with the dump_source.