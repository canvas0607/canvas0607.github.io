---
layout: post
title:  "mongodb aggregation facet use"
date:   2021-07-04 16:00:00 +0800
categories: mongodb
---

### 1. describe
Processes multiple aggregation pipelines within a single stage on the same set of input documents. Each sub-pipeline has its own field in the output document where its results are stored as an array of documents.

The facet stage has the following form:

```angular2html

{ $facet:
   {
      <outputField1>: [ <stage1>, <stage2>, ... ],
      <outputField2>: [ <stage1>, <stage2>, ... ],
      ...

   }
}
```

usually use those three methods

$bucket
$bucketAuto
$sortByCount


### 2. sortByCount

this stage can replace group and sum:$1 

using atlas mongodb,db sample_training ,collection companies

```angular2html

result = client['sample_training']['companies'].aggregate([
    {
        '$sortByCount': '$category_code'
    }
])

```

the result can be grouped category_code and count their nums

```angular2html

{_id:"web"
count:1947
}
{_id:null
count:1407
}
{_id:"software"
count:1356
}
{_id:"games_video"
count:528
}
```

more complicated query

```angular2html

db.companies.aggregate([
  {"$match": { "$text": {"$search": "network"}  }  } ,
  {"$unwind": "$offices"},
  {"$match": { "offices.city": {"$ne": ""}  }}   ,
  {"$sortByCount": "$offices.city"}] )

```
### bucket and auto bucket

```
# create manual buckets using $ bucket
mongo startups --eval '
db.companies.aggregate( [
  { "$match": {"founded_year": {"$gt": 1980}, "number_of_employees": {"$ne": null}}  },
  {"$bucket": {
     "groupBy": "$number_of_employees",
     "boundaries": [ 0, 20, 50, 100, 500, 1000, Infinity  ]}
}] )
'
``` 

if this is other type of value,default must be set

reproduce error message for non matching documents
```
# reproduce error message for non matching documents
mongo startups --eval '
db.coll.insert({ x: "a" });
db.coll.aggregate([{ $bucket: {groupBy: "$x", boundaries: [0, 50, 100]}}])
'

# set `default` option to collect documents that do not match boundaries
mongo startups --eval '
db.companies.aggregate( [
  { "$match": {"founded_year": {"$gt": 1980}}},
  { "$bucket": {
    "groupBy": "$number_of_employees",
    "boundaries": [ 0, 20, 50, 100, 500, 1000, Infinity  ],
    "default": "Other" }
}] )

```
output can add fields where values grouped

```angular2html

db.companies.aggregate([
  { "$match":
    {"founded_year": {"$gt": 1980}}
  },
  { "$bucket": {
      "groupBy": "$number_of_employees",
      "boundaries": [ 0, 20, 50, 100, 500, 1000, Infinity  ],
      "default": "Other",
      "output": {
        "total": {"$sum":1},
        "average": {"$avg": "$number_of_employees" },
        "categories": {"$addToSet": "$category_code"}
      }
    }
  }
]
)

```

bucketAuto will automatically split the length

```angular2html

'db.companies.aggregate([
  { "$match": {"offices.city": "New York" }},
  {"$bucketAuto": {
    "groupBy": "$founded_year",
    "buckets": 5,
    "output": {
        "total": {"$sum":1},
        "average": {"$avg": "$number_of_employees" }  }}}
])
```
granularity

```angular2html

# generate automatic buckets using granularity numerical series R20
mongo startups --eval 'db.series.aggregate(
  {$bucketAuto:
    {groupBy: "$_id", buckets: 5 , granularity: "R20"}
  })

```

facet using those stage multiply

```angular2html

mongo startups --eval 'db.companies.aggregate( [
    {"$match": { "$text": {"$search": "Databases"} } },
    { "$facet": {
      "Categories": [{"$sortByCount": "$category_code"}],
      "Employees": [
        { "$match": {"founded_year": {"$gt": 1980}}},
        {"$bucket": {
          "groupBy": "$number_of_employees",
          "boundaries": [ 0, 20, 50, 100, 500, 1000, Infinity  ],
          "default": "Other"
        }}],
      "Founded": [
        { "$match": {"offices.city": "New York" }},
        {"$bucketAuto": {
          "groupBy": "$founded_year",
          "buckets": 5   }
        }
      ]
  }}]).pretty()

```

usage

How many movies are in both the top ten highest rated movies according to the imdb.rating and the metacritic fields? 
We should get these results with exactly one access to the database.

```angular2html

db.movies.aggregate([
  {
    $match: {
      metacritic: { $gte: 0 },
      "imdb.rating": { $gte: 0 }
    }
  },
  {
    $project: {
      _id: 0,
      metacritic: 1,
      imdb: 1,
      title: 1
    }
  },
  {
    $facet: {
      top_metacritic: [
        {
          $sort: {
            metacritic: -1,
            title: 1
          }
        },
        {
          $limit: 10
        },
        {
          $project: {
            title: 1
          }
        }
      ],
      top_imdb: [
        {
          $sort: {
            "imdb.rating": -1,
            title: 1
          }
        },
        {
          $limit: 10
        },
        {
          $project: {
            title: 1
          }
        }
      ]
    }
  },
  {
    $project: {
      movies_in_both: {
        $setIntersection: ["$top_metacritic", "$top_imdb"]
      }
    }
  }
])

```
	
# link

1. https://docs.mongodb.com/manual/reference/operator/aggregation/facet/
2. https://blog.csdn.net/weixin_41422810/article/details/103785346
	