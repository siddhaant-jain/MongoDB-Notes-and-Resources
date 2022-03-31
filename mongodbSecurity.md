- authorization (check if user is valid for the given database)
- authentication (check what actions can user perform on the given database)
- mongodb implements RBAC(Role Based Access Control)

## Roles in MongoDB
- different type of users:
    - Administrator - creating DB, managing users etc.
    - Developer / App - CRUD access
    - User (Data Scientist) - only read access

- creating and editing a user
    - createUser() command, updateUser() command
    - each user has a role and corresponding privelages.
    - users are attached to databased

- we can sign in to mongo shell in two ways
    - first is to simply open mongo shell with 'mongo' command and then run db.auth(username, password)
    - second way is to write it in command itself like this: mongo -u username -p password --authenticationDatabase admin

- create new user when no user is created so far
    - open mongo shell without authentication
    > use admin
    > db.createUser({user: "username", pwd: "password", roles: ["userAdminAnyDatabase"]})

- built in roles
    - Database user (read, readWrite)
    - Database admin (dbAdmin, userAdmin, dbOwner)
    - All Database Roles (above two user can get more roles from below mentioned list):
        - readAnyDatabase
        - readWriteAnyDatabase
        - userAdminAnyDatabase
        - dbAdminAnyDatabase
    - cluster admin
    - backup/restore
    - superUser (create and change users)

- create user for a database
    ```
    use database_for_which_we_are_creating_user
    db.createUser({user: "username", pwd: "password", roles: ["readWrite"]})
    db.logout() (alternatively we can exit out of mongo shell)
    mongo -u username -p password --authenticationDatabase database_for_which_we_are_creating_user
    ```

- to see all details of a user
    > db.getUser("username")

- one user should be able to access multiple databases
- we can update the existing user:
    ```
    db.logout()
    use admin
    db.auth('usernameOnAdminDb', 'passwordOnAdminDb')
    use db_which_already_has_the_user
    db.updateUser("usernameOfUserWeWantToUpdate", {
        roles: ["readWrite", {role: "readWrite", db: "blog"}]
    })
    ```

- first argument in update is username of the user we want to update
- second arg can be pwd also, but we want to modify the roles
- whatever we mention, will replace existing role array, so we should first repeat the existing thing
- second element is the new role we wanted to add, same permission but on a different db this time


# Performace and Fault Tolerance in mongodb
- what influences performance?
    - affected by developers, db admin
        - efficient queries
        - using indexing
        - fitting data schema (if data is stored in a way that we always have to perform lot of aggregations and transformations, then that may affect thee prformance)
    - affected by network etc.
        - hardware and network
        - replica sets
        - sharding

- capped collections
- special collections where we limit the amount of data or number of documents that'll be stored
- so old data is automatically deleted when new data comes
- to define a capped collection:
    > db.createCollection("collectionName", {capped: true, size: 10000, max:4})
- by default the size is 4 bytes
- max defines the maximum number of documents it'll store (this is optional)
- if we insert a 5th element, the element which was inserted 1st will be deleted and so on\
- this collection is always sorted by insertion order

- replica set
- mongo server is connected to the primary node which contains all the data by default
- when we write a query to insert or update, it automatically is done on primary node
- but we can add multiple secondary nodes as well
- data is asyncronously (not immediately) replicated from primary node to all the secondary nodes
- this is done so that if primary node is down then one of the secondary node is voted new primary node
- this helps in fault tolerancy
- it also improves read performance (we can distribute read requests among all nodes, writes will still go to primary node only)

- sharding (horizontal scaling)
- in sharding we have multiple servers splitting the data among themselves (distributed)
- this is different from replica where other servers are basically backups of the primary one
- Queries are run across all servers
- each of these shards/servers can have their own replica sets
- with sharding we need to have a middlemen called 'mongos' which is a Router
- it forwards operations to the right shards.
- bcz every document will now have a shard key which is carefully chosen so that data is evenly distributed.
- if mongos is not able to get the shard keys, it broadcasts the query to all the shards.

- deploying a mongodb server (to web)
- done using mongodb atlas

- transactions
- all operations either succeed together or fail together
- can be done by creating a session
- a session groups all the commands together
- with session we can start and stop a transaction
- until we have commit the session no command is really execute. it is simply acknowledged and stored in a sort of TODO list.
- we can also do session.abortTransaction() to rollback everything you've done in current session
- for a single query mongodb already ensures atomicity, transactions help in maintaining this for a group of queries.