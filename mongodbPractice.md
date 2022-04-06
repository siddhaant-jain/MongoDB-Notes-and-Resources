Link to [Questions](https://www.w3resource.com/mongodb-exercises/)

### sample data (restaurants)
    ```javascript
    {
    "address": {
        "building": "1007",
        "coord": [ -73.856077, 40.848447 ],
        "street": "Morris Park Ave",
        "zipcode": "10462"
    },
    "borough": "Bronx",
    "cuisine": "Bakery",
    "grades": [
        { "date": { "$date": 1393804800000 }, "grade": "A", "score": 2 },
        { "date": { "$date": 1378857600000 }, "grade": "A", "score": 6 },
        { "date": { "$date": 1358985600000 }, "grade": "A", "score": 10 },
        { "date": { "$date": 1322006400000 }, "grade": "A", "score": 9 },
        { "date": { "$date": 1299715200000 }, "grade": "B", "score": 14 }
    ],
    "name": "Morris Park Bake Shop",
    "restaurant_id": "30075445"
    }
    ```

### Complete dataset
[FullDataset](https://raw.githubusercontent.com/mongodb/docs-assets/primer-dataset/dataset.json)

> mongoimport restaurantsmongoDbList.json -d siddhant -c restaurant --jsonArray --drop -u "admin" -p "pass" --authenticationDatabase admin

1. Write a MongoDB query to display all the documents in the collection restaurants
    > db.restaurants.find({})

2. Write a MongoDB query to display the fields restaurant_id, name, borough and cuisine for all the documents in the collection restaurant.
    > db.restaurants.find({}, {restaurant_id: 1, name:1, borough:1, cuisine:1})

3. Write a MongoDB query to display the fields restaurant_id, name, borough and cuisine, but exclude the field _id for all the documents in the collection restaurant.
    > db.restaurants.find({}, {_id:0, restaurant_id: 1, name:1, borough:1, cuisine:1})

4. Write a MongoDB query to display the fields restaurant_id, name, borough and zip code, but exclude the field _id for all the documents in the collection restaurant.
    > db.restaurants.find({}, {restaurant_id: 1, name:1, borough:1, "address.zipcode":1})

5. Write a MongoDB query to display all the restaurant which is in the borough Bronx.
    > db.restaurants.find({borough: 'Bronx'})

6. Write a MongoDB query to display the first 5 restaurant which is in the borough Bronx.
    > db.restaurants.find({borough: 'Bronx'}).limit(5)

7. Write a MongoDB query to display the next 5 restaurants after skipping first 5 which are in the borough Bronx.
    > db.restaurants.find({borough: 'Bronx'}).skip(5).limit(5)

8. Write a MongoDB query to find the restaurants who achieved a score more than 90.
    - wrong approach (if there we multiple condition on same array element (element can be document also))
    > ~~db.restaurant.find({"grades.score": {$gt: 90}})~~
    - right approach
    > db.restaurant.find({grades: {$elemMatch: {score: {$gt: 90}}}})

9. Write a MongoDB query to find the restaurants that achieved a score, more than 80 but less than 100
    - wrong query (it will match any element with even one condition satisfied, since less than 100 will be true for most, it will return almost all docs)
    > ~~ db.restaurant.find({grades: {$elemMatch: {score: {$gt: 80}, score: {$lt: 100}}}}).count() ~~
    - right query:
    > db.restaurant.find({grades : { $elemMatch:{"score":{$gt : 80 , $lt :100}}}});

10. Write a MongoDB query to find the restaurants which locate in latitude value less than -95.754168.
    > db.restaurant.find({"address.coord.0": {$lt: -95.754168}})

11. Write a MongoDB query to find the restaurants that do not prepare any cuisine of 'American' and their grade score more than 70 and latitude less than -65.754168
    ```javascript
    db.restaurant.find({
        $and: [
            {cuisine: {$ne: 'American'}},
            {grades: {$elemMatch: {score: {$gt: 70}}}},
            {"address.coord.0": {$lt: -65.754168}}
        ]
    })
    ```

12. Write a MongoDB query to find the restaurants which do not prepare any cuisine of 'American' and achieved a score more than 70 and located in the longitude less than -65.754168.
Note : Do this query without using $and operator
    ```javascript
    db.restaurant.find({
        cuisine: {$ne: "American"},
        "grade.score": {$gt: 70},
        "address.coord.1": {$lt: -65.754168}
    })
    ```

13. Write a MongoDB query to find the restaurants which do not prepare any cuisine of 'American ' and achieved a grade point 'A' not belongs to the borough Brooklyn. The document must be displayed according to the cuisine in descending order.
    ```javascript
    db.restaurant.find({
        cuisine: {$ne: "American"},
        "grades.grade": "A",
        borough: {$ne: "Brooklyn"}
    }).sort({cuisine: -1})
    ```

14. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which contain 'Wil' as first three letters for its name.
    - my solution
        ```javascript
        db.restaurant.aggregate(
        {
            $project: {
                restaurant_id: 1,
                name: 1,
                borough: 1,
                cuisine: 1,
                _id: 0,
                nameSub: {$substrCP: ['$name', 0, 3]} 
            }
        },
        {
            $match: {
                nameSub: 'Wil'
            }
        },
        {
            $project: {
                restaurant_id: 1,
                name: 1,
                borough: 1,
                cuisine: 1,
                _id: 0
            }
        },
        <!-- {
            $group: {
                _id: {rest_id: "restaurant_id"},
                totalCount: {$sum: 1}
            }
        } -->
        )
        ```
    - alternate solution (using regex) (both giving same count of 31 docs)
    ```javascript
    db.restaurant.find(
        {name: /^Wil/},
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    );

15. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which contain 'ces' as last three letters for its name.
    - solution 1
    ```javascript
    db.restaurant.find(
        {name: /ces$/},
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    )
    ```

    - solution 2
    ```javascript
        db.restaurant.aggregate(
        {
            $project: {
                restaurant_id: 1,
                name: 1,
                borough: 1,
                cuisine: 1,
                _id: 0,
                nameLen: {$strLenCP: '$name'}
            }
        },
        {
            $match: {nameLen: {$gte: 3}}
        },
        {
            $project: {
                restaurant_id: 1,
                name: 1,
                borough: 1,
                cuisine: 1,
                _id: 0,
                nameSub: {$substrCP: [
                    '$name', 
                    {$subtract: [
                        {$strLenCP: '$name'},
                        3
                    ]},
                    3]} 
            }
        },
        {
            $match: {
                nameSub: 'ces'
            }
        },
        {
            $project: {
                restaurant_id: 1,
                name: 1,
                borough: 1,
                cuisine: 1,
                _id: 0
            }
        },
        {
            $group: {
                _id: {rest_id: "restaurant_id"},
                totalCount: {$sum: 1}
            }
        }
        )
        ```

16. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which contain 'Reg' as three letters somewhere in its name
    ```javascript
    db.restaurant.find(
        {name: /.*Reg.*/},
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    );
    ```
    
17. Write a MongoDB query to find the restaurants which belong to the borough Bronx and prepared either American or Chinese dish.
    ```javascript
    db.restaurant.find(
        {
            $and: [
                {borough: 'Bronx'},
                {$or: [{cuisine: 'American'}, {cuisine: 'Chinese'}]}
            ]
        }
    );
    ```

18. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which belong to the borough Staten Island or Queens or Bronxor Brooklyn
    ```javascript
    db.restaurant.find(
        {
            borough: {
                $in: [
                    'Staten Island',
                    'Queens',
                    'Bronxor Brooklyn'
                ]
            }
        },
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    ).count();
    ```

19. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which are not belonging to the borough Staten Island or Queens or Bronxor Brooklyn.
    ```javascript
    db.restaurant.find(
        {
            borough: {
                $nin: [
                    'Staten Island',
                    'Queens',
                    'Bronxor Brooklyn'
                ]
            }
        },
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    ).count();
    ```

20. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which achieved a score which is not more than 10.
    - wrong. 
    - This may include array elements more than 10 but, one element should be less than 10. In that case, this query will match but this is not what asked in this problem.
    ```javascript
    db.restaurant.find(
        {
            "grades.score": {$lte: 10}
        },
        {
        "restaurant_id" : 1,
        "name":1,"borough":1,
        "cuisine" :1
        }
    ).count();
    ```
    - correct,
    - This finds array having objects { $gt: 10 } which means it may include $lt:10 but, one element must be greater than 10.After that, using $not, query will exclude all the objects found by { $gt: 10 }. Hence we will get correct output where each and every element of an array should be less than 10.
    ```javascript
    db.restaurant.find(
        {
            "grades.score" : 
            { $not: 
                {$gt : 10}
            }
        },
        {
            "restaurant_id" : 1,
            "name":1,"borough":1,
            "cuisine" :1
        }
    ).count();
    ```

21. Write a MongoDB query to find the restaurant Id, name, borough and cuisine for those restaurants which prepared dish except 'American' and 'Chinees' or restaurant's name begins with letter 'Wil'
    - my solution
    ```javascript
    db.restaurant.find(
        {
           $or: [
               {cuisine: {$nin: ['American', 'Chinees']}},
               {name: '/^Wil/'}
           ]
        },
        {
            "restaurant_id" : 1,
            "name":1,"borough":1,
            "cuisine" :1
        }
    ).count();
    ```

    - solution on the website (giving different count)
    ```javascript
    db.restaurant.find(
        {$or: [
            {name: /^Wil/}, 
            {"$and": [
                {"cuisine" : {$ne :"American "}}, 
                {"cuisine" : {$ne :"Chinees"}}
            ]}
        ]}
        ,{"restaurant_id" : 1,"name":1,"borough":1,"cuisine" :1}
    );
    ```

22. Write a MongoDB query to find the restaurant Id, name, and grades for those restaurants which achieved a grade of "A" and scored 11 on an ISODate "2014-08-11T00:00:00Z" among many of survey dates.
    ```javascript
    db.restaurant.find(
        {
            grades: {
                $elemMatch: {
                    grade: "A",
                    score: {$gt: 11},
                    date: ISODate("2014-08-11T00:00:00Z")
                }
            }
        }
        ,{"restaurant_id" : 1,"name":1,"grades":1}
    ).count();
    ```

23. Write a MongoDB query to find the restaurant Id, name and grades for those restaurants where the 2nd element of grades array contains a grade of "A" and score 9 on an ISODate "2014-08-11T00:00:00Z"
    ```javascript
    db.restaurant.find(
        {
            "grades.1.grade": "A",
            "grades.1.score": 9,
            "grades.1.date": ISODate("2014-08-11T00:00:00Z")
        }
        ,{"restaurant_id" : 1,"name":1,"grades":1}
    ).count();
    ```

24. Write a MongoDB query to find the restaurant Id, name, address and geographical location for those restaurants where 2nd element of coord array contains a value which is more than 42 and upto 52.
    ```javascript
    db.restaurant.find(
        {
            "address.coord.1": {$gt: 42, $lte:52}
        }
        ,{"restaurant_id" : 1,"name":1,"address":1}
    ).count();
    ```

25. Write a MongoDB query to arrange the name of the restaurants in ascending order along with all the columns.
    ```javascript
    db.restaurant.find().sort({name: 1});
    ```

26. Write a MongoDB query to arrange the name of the restaurants in descending along with all the columns
    ```javascript
    db.restaurant.find().sort({name: -1});
    ```

27. Write a MongoDB query to arranged the name of the cuisine in ascending order and for that same cuisine borough should be in descending order. 
    ```javascript
    db.restaurant.find().sort({cuisine: 1, borough: -1});
    ```

28. Write a MongoDB query to know whether all the addresses contains the street or not
    ```javascript
    db.restaurant.find({"address.street": {$exists: false}}).count()
    ```

29. Write a MongoDB query which will select all documents in the restaurants collection where the coord field value is Double
    - my solution
    ```javascript
    db.restaurant.find(
        {
            $and: [
                {"address.coord.0": {$type: "double"}},
                {"address.coord.1": {$type: "double"}}
            ]
        }
    ).count()
    ```

    - solution on site (same result)
    ```javascript
    db.restaurant.find(
        {
            "address.coord" : {$type : 1}
        }
    );
    ```

30. Write a MongoDB query which will select the restaurant Id, name and grades for those restaurants which returns 0 as a remainder after dividing the score by 7.
    - website solution (didn't know about mod)
    ```javascript
    db.restaurant.find(
        {
            "grades.score" : {$mod : [7,0]}
        }
        ,{"restaurant_id" : 1,"name":1,"grades":1}
    ).count();
    ```

31. Write a MongoDB query to find the restaurant name, borough, longitude and attitude and cuisine for those restaurants which contains 'mon' as three letters somewhere in its name.
    - didn't know, website solution
    ```javascript
    db.restaurant.find(
        {
            name: {$regex: ".*mon.*", $options: 'i'}
        }
        ,{"name":1,"borough":1, "address.coord.0": 1,"address.coord.1": 1, "cuisine":1}
    ).count();
    ```

32. Write a MongoDB query to find the restaurant name, borough, longitude and latitude and cuisine for those restaurants which contain 'Mad' as first three letters of its name.
    ```javascript
    db.restaurant.find(
        {
            name: {$regex: "^Mad.*"}
        }
        ,{"name":1,"borough":1, "address.coord.0": 1,"address.coord.1": 1, "cuisine":1}
    ).count();
    ```
    