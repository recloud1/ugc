#!/bin/bash
set -e

mongosh <<EOF
use admin
const dbName = '$MONGO_NAME';
const conn = new Mongo();
const db = conn.getDB(dbName);

const collections = [
    "movie",
    'users',
    "likes",
    "reviews",
    "bookmarks"
];

collections.forEach((collection) => {
    db.createCollection(collection);
});
EOF
