- importing person.json file
    > mongoimport persons.json -d siddhant -c contacts --jsonArray --drop -u "admin" -p "pass" --authenticationDatabase admin

- instead of using .find() command we use .aggregate() commmand
- it takes a list as argument, which is a series of steps that need to be performed in sequential order

## Different stages of aggregation framework
- we can have same stage multiple times also
- one of the stage in the list can be '$match' command which is similar to find
    ```javascript
    db.contacts.aggregate([
        {$match: {gender: "male"}}
    ])
    ```

- another stage can be '$group' stage
- below command will find count of all females state-wise
    ```javascript
    db.contacts.aggregate([
        {$match: {gender: "male"}},
        {$group: {_id: {state: "$location.state"}, totalPersons: {$sum: 1}}}
    ])
    ```

- another stage can be '$sort' stage
    ```javascript
    db.contacts.aggregate([
        {$match: {gender: "male"}},
        {$group: {_id: {state: "$location.state"}, totalPersons: {$sum: 1}}},
        {$sort: {totalPersons: -1}}
    ])
    ```

- each stage in aggregation framework has only the data from the previous stage
    - first stage takes input data as prev stage
    - so group will have only contacts data will documents containing gender as female
    - and sort will have only two columns state and totalPersons which it receives from group stage

- '$project' stage
- it is similar to project in find method
- if we simply want to include or exclude a specific column we can do that by 1/0 respecetively
- we can create new columns also on the fly by giving new column name and then using functions like '$concat'
- we can make it more complex by adding more methods like '$upper'
    ```javascript
    db.contacts.aggregate([
        {
            $project: 
            {
                _id: 0, 
                gender: 1, 
                fullName: {
                    $concat: [
                        {$toUpper: "$name.first"}, 
                        " ", 
                        {$toUpper: "$name.last"}
                    ]
                }
            }
        }
    ])
    ```
- final use case is to make only the first letter of both words uppers and not the entire string
    ```javascript
    db.contacts.aggregate([
        {
            $project: 
            {
                _id: 0, 
                gender: 1, 
                fullName: {
                    $concat: [
                        {$toUpper: {$substrCP: ['$name.first', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.first', 
                                1, 
                                {$subtract: [{$strlenCP: "$name.first"},1]}
                            ]
                        },
                        " ", 
                        {$toUpper: {$substrCP: ['$name.last', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.last', 
                                1, 
                                {$subtract: [{$strlenCP: "$name.last"},1]}
                            ]
                        }
                    ]
                }
            }
        }
    ])
    ```
- to get only first letter as capital we break the string into two parts
- using '$substrCP' we get the substring which takes 3 parameters: column_name, starting_pos, number of characters to take
- for first letter this will become column_name = $name.first, starting_pos = 0, number of characters to take = 1, this will be converted to upper-case
- for rest of the substring we know starting position is 1, and number of characters is total_length-1, since one character is used in prev. substring
- for that we can usee $substract which takes a list of two args and does arg1-arg2
- to get length, we use 'strlenCP' command which takes column name of which we need te length

## Converting a column containg coordinates into a geoJson object using projections
- sample location data in actual dataset look like:
    ```json
    "location" : {
        "street" : "3193 king st",
        "city" : "chipman",
        "state" : "yukon",
        "postcode" : "H8N 1Q8",
        "coordinates" : {
                "latitude" : "76.4507",
                "longitude" : "-70.2264"
        },
        "timezone" : {
                "offset" : "+11:00",
                "description" : "Magadan, Solomon Islands, New Caledonia"
        }
    }
    ```
- final output should also contain email
- and flatten dob so that it has a birthdate and age. sample dob data in actual dataset look like:
    ```json
    "dob" : {
        "date" : "1988-10-17T03:45:04Z",
        "age" : 29
    }
    ```

- code to the above mentioned things:
    ```javascript
    db.contacts.aggregate([
        {
            $project: 
            {
                _id: 0,
                name: 1, 
                gender: 1,
                email: 1,
                locationGeoJson: {type: 'Point', coordinates: [
                    {
                        $convert:
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    },
                    {
                        $convert: 
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    }
                ]},
                birthDate : {
                    '$dob.date'
                },
                age: {
                    '$dob.age'
                }
            }
        },
        {
            $project: 
            {
                gender: 1,
                email: 1,
                locationGeoJson: 1,
                fullName: {
                    $concat: [
                        {$toUpper: {$substrCP: ['$name.first', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.first', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.first"},1]}
                            ]
                        },
                        " ", 
                        {$toUpper: {$substrCP: ['$name.last', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.last', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.last"},1]}
                            ]
                        }
                    ]
                },
                birthDate: 1,
                age: 1
            }
        }
    ]).pretty()
    ```

- adding the flat fields for birthDate and age in correct formats
    ```javascript
    db.contacts.aggregate([
        {
            $project: 
            {
                _id: 0,
                name: 1, 
                gender: 1,
                email: 1,
                locationGeoJson: {type: 'Point', coordinates: [
                    {
                        $convert:
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    },
                    {
                        $convert: 
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    }
                ]},
                birthDate : {
                    $dateFromString : {
                        dateString: '$dob.date',
                        format: "%Y-%m-%dT%H:%M:%SZ",
                        onError: '$dob.date',
                        onNull: new Date(0)
                    }
                },
                age: '$dob.age',
            }
        },
        {
            $project: 
            {
                gender: 1,
                email: 1,
                locationGeoJson: 1,
                fullName: {
                    $concat: [
                        {$toUpper: {$substrCP: ['$name.first', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.first', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.first"},1]}
                            ]
                        },
                        " ", 
                        {$toUpper: {$substrCP: ['$name.last', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.last', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.last"},1]}
                            ]
                        }
                    ]
                },
                birthDate: 1,
                age: 1
            }
        }
    ]).pretty()
    ```

- adding a group stage to above data and group by birth year
    ```javascript
    db.contacts.aggregate([
        {
            $project: 
            {
                _id: 0,
                name: 1, 
                gender: 1,
                email: 1,
                locationGeoJson: {type: 'Point', coordinates: [
                    {
                        $convert:
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    },
                    {
                        $convert: 
                        {
                            input:"$location.coordinates.longitude", 
                            to: 'double', onError: 0.0, onNull: 0.0
                        }
                    }
                ]},
                birthDate : {
                    $dateFromString : {
                        dateString: '$dob.date',
                        format: "%Y-%m-%dT%H:%M:%SZ",
                        onError: '$dob.date',
                        onNull: new Date(0)
                    }
                },
                age: '$dob.age',
            }
        },
        {
            $project: 
            {
                gender: 1,
                email: 1,
                locationGeoJson: 1,
                fullName: {
                    $concat: [
                        {$toUpper: {$substrCP: ['$name.first', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.first', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.first"},1]}
                            ]
                        },
                        " ", 
                        {$toUpper: {$substrCP: ['$name.last', 0, 1]}}, 
                        {
                            $substrCP: [
                                '$name.last', 
                                1, 
                                {$subtract: [{$strLenCP: "$name.last"},1]}
                            ]
                        }
                    ]
                },
                birthDate: 1,
                age: 1
            }
        },
        {
            $group: {
                _id: {
                    birthYear: {$isoWeekYear: '$birthDate'}
                },
                numberOfPersons: {$sum: 1}
            }
        },
        {
            $sort: {numberOfPersons: -1}
        }
    ])
    ```

- create new collection for array-based on operations in aggregations
    ```javascript
    db.friends.insertMany([
        {
            "name": "Max",
            "hobbies": ["Sports", "Cooking"],
            "age": 29,
            "examScores": [
            { "difficulty": 4, "score": 57.9 },
            { "difficulty": 6, "score": 62.1 },
            { "difficulty": 3, "score": 88.5 }
            ]
        },
        {
            "name": "Manu",
            "hobbies": ["Eating", "Data Analytics"],
            "age": 30,
            "examScores": [
            { "difficulty": 7, "score": 52.1 },
            { "difficulty": 2, "score": 74.3 },
            { "difficulty": 5, "score": 53.1 }
            ]
        },
        {
            "name": "Maria",
            "hobbies": ["Cooking", "Skiing"],
            "age": 29,
            "examScores": [
            { "difficulty": 3, "score": 75.1 },
            { "difficulty": 8, "score": 44.2 },
            { "difficulty": 6, "score": 61.5 }
            ]
        }
    ])
    ```

- push new elements to an array 
    ```javascript
    db.friends.aggregate([
        {
            $group: {_id: {age: "$age"}, allHobbiesForThisAge: {$push: "$hobbies"}}
        }
    ])
    ```

- $ push works with any column, not just array columns
- if we use it with name, it will create an array of names for each age
- above statement will just make it an array of array, each hobbies array will be pushed as an element
- we want to add individual elements (using $unwind)
    ```javascript
    db.friends.aggregate([
        {
            $unwind: "$hobbies"
        },
        {
            $group: {_id: {age: "$age"}, allHobbiesForThisAge: {$push: "$hobbies"}}
        }
    ])
    ```

- if we simply run the unwind stage for one document it will create multiple document with column holding only one of the array values at a time. 
- eg. {name:a, other: [1,2,3]} if we unwind this doc, it will become {name:a, other: 1}, {name:a, other: 2}, {name:a, other: 3}
- above code will still have one issue ... after grouping there can be duplicates if same element is repeating across multiple docuemnts ('cooking' in this example)
- we can solve this with $addToSet which is similar to $push but doesn't allow duplicates
    ```javascript
    db.friends.aggregate([
        {
            $unwind: "$hobbies"
        },
        {
            $group: {_id: {age: "$age"}, allHobbiesForThisAge: {$addToSet: "$hobbies"}}
        }
    ])
    ```

- projection on arrays - $slice -> takes 1 element from 2nd element
    ```javascript
    db.friends.aggregate([
        {
            $project: {
                _id:0,
                examScore: {$slice: ['$examScores',2,1]}
            }
        }
    ])
    ```

- finding length of array
    ```javascript
    db.friends.aggregate([
        {
            $project: {
                _id:0,
                numOfExams: {$size: "$examScores"} 
            }
        }
    ])
    ```

- $filter operator
    ```javascript
    db.friends.aggregate([
        {
            $project: {
                _id:0,
                examScore: {$filter: {input: "$examScores", as: "sc", cond: {
                    $gt: ["$$sc.score", 60 ]
                    }
                }}
            }
        }
    ])
    ```

- multiple operations on array (want max score for each person)
    ```javascript
    db.friends.aggregate([
        {
            $unwind: "$examScores"
        },
        {
            $project: {
                _id:1,
                name:1,
                age: 1,
                score: '$examScores.score'
            }
        },
        {
            $sort: {score:-1}
        },
        {
            $group: {
                _id: {name: "$_id"},
                name: {$first: "$name"},
                maxScore: {$max: "$score"}
            }
        },
        {
            $sort: {maxScore: -1}
        }
    ])
    ```
- since we're only grouping on id, we can't directly print the name without any aggregation, so we use $first which tell to take first name from each id group (since here name is unique for each id)

- $bucket operator - to see distribution of data
    ```javascript
    db.contacts.aggregate([
        {
            $bucket: {
                groupBy: "$dob.age", 
                boundaries: [0,18,30,50,80,120], 
                output: {
                    numPerson: {$sum: 1},
                    avgAge: {$avg: "$dob.age"}
                }
            }
        }
    ])
    ```

- we can aslo have $bucketAuto where mongodb decides where to draw the boundaries, we just tell the number of buckets we want
    ```javascript
    db.contacts.aggregate([
        {
            $bucketAuto: {
                groupBy: "$dob.age", 
                bucket: 5, 
                output: {
                    numPerson: {$sum: 1},
                    avgAge: {$avg: "$dob.age"}
                }
            }
        }
    ])
    ```
- aprt of other outputs, it also tell left and right end of the bound

- we can add limt and skip as stages in aggregate also
- in find method order of sort, skip and limit didn't matter. it always ran in this mentioned order
- but in aggregate it matters, bcz each stage runs after the previous one
- so if we first limit to 10 and then skip 10, we'll get blank result since bcz of limit only 10 records were givien to skip as data which it skipped


- writing output of a pipeline to another collection
    ```javascript
    db.contacts.aggregate([
        {
            $bucketAuto: {
                groupBy: "$dob.age", 
                bucket: 5, 
                output: {
                    numPerson: {$sum: 1},
                    avgAge: {$avg: "$dob.age"}
                }
            }
        },
        {
            $out: "newOrExistingCollection"
        }
    ])
    ```