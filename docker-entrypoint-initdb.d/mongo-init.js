
print('Start creating database ##########################')
db = db.getSiblingDB('flask_mongo_test');
db.createUser(
    {
        user: 'flask_user',
        pwd:  'flask_pass',
        roles: [{role: 'readWrite', db: 'flask_mongo_test'}],
    }
);
print('End creating database ##########################')