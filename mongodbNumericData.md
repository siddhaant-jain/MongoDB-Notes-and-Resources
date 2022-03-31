- types of numeric data
    - int (-2,147,483,648 to +2,147,483,647)
    - long (-9,223,372,036,854,775,808 to +-9,223,372,036,854,775,807)
    - double (low precision - stores approximate values)
    - high precision double (high precision)

- default data type for numeric is not decided by mongodb but the client on which we are using mongodb
- for example in javascript or mongo shell (which is based in javascript) even if we give an integer input like 38 it will be stored as a low precision double. So internally it will become something like 64.00002
- but if we are using python where it can diffrentiate between 1 and 1.0, this value (38) will get stored as an int


