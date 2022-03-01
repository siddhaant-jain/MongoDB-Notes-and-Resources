# All commands in mongo shell

## basic db commands
- create a database
    > use \<dbname>
    > eg. use flights
- create a collections in database
- use a database
- list all databases
- list all collections in current database
- see which database we are currently using
- drop a collection
    > db.collection_name.drop()
- to get all statistics about a database
    > db.stats() #while in current database
- see datatype of a particular column
    > typeof db.collection_name.findOne().keyName

## crud operations
### create operations
- insert one (data, options)
    > db.collectionName.insertOne({document to insert})
- insert many (data, options)
    > db.collectionName.insertMany([list of documents in square brackets])

### read operations
- find (fiter, options)
- find one (filter, options)
- find to Array (to get all results at once in form of an array)(we can also use foreach with this)
     > db.collectionName.find().toArray()

### update operations
- update one (fiter, data, options)
- update many (fiter, data, options)
- update
- replace one (fiter, data, options)
- replace many (fiter, data, options)

### delete operations
- delete one (fiter, options)
- delete many (fiter, options)
- delete all records in a collection
> db.collectionName.deleteMany({})

### projection
- 1, 0


