#!/usr/bin/env python3
"""
API Coverage & Parity Matrix Data Collection Script
Collects data about database vendor API capabilities across SQL, KV, Document, Graph, and Search
"""

import csv
import json
import requests
from datetime import datetime
from typing import List, Dict, Any

# Target schema: vendor, api, feature, status{GA|Preview|NA}, added_date, doc_url

def collect_aws_data() -> List[Dict[str, Any]]:
    """Collect AWS database service API coverage data"""
    data = []
    
    # DynamoDB
    dynamodb_features = [
        # CRUD Operations
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "GetItem", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html"},
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "PutItem", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html"},
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "UpdateItem", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html"},
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "DeleteItem", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html"},
        {"vendor": "AWS", "api": "DynamoDB-Document", "feature": "Query", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html"},
        {"vendor": "AWS", "api": "DynamoDB-Document", "feature": "Scan", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html"},
        {"vendor": "AWS", "api": "DynamoDB-SQL", "feature": "PartiQL-SELECT", "status": "GA", "added_date": "2020-11-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html"},
        {"vendor": "AWS", "api": "DynamoDB-SQL", "feature": "PartiQL-INSERT", "status": "GA", "added_date": "2020-11-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html"},
        {"vendor": "AWS", "api": "DynamoDB-SQL", "feature": "PartiQL-UPDATE", "status": "GA", "added_date": "2020-11-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html"},
        {"vendor": "AWS", "api": "DynamoDB-SQL", "feature": "PartiQL-DELETE", "status": "GA", "added_date": "2020-11-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html"},
        
        # Indexing
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "Global-Secondary-Index", "status": "GA", "added_date": "2013-04-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html"},
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "Local-Secondary-Index", "status": "GA", "added_date": "2013-04-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html"},
        
        # Pagination
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "Pagination-Token", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html#Query.Pagination"},
        
        # Transactions
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "ACID-Transactions", "status": "GA", "added_date": "2018-11-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html"},
        
        # Consistency
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "Eventually-Consistent-Read", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html"},
        {"vendor": "AWS", "api": "DynamoDB-KV", "feature": "Strongly-Consistent-Read", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html"},
        
        # Cross-API capabilities
        {"vendor": "AWS", "api": "DynamoDB-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "DynamoDB-Search", "feature": "Full-Text-Search", "status": "NA", "added_date": "", "doc_url": ""},
    ]
    
    # RDS (Relational)
    rds_features = [
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "SELECT", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "INSERT", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "UPDATE", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "DELETE", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "B-Tree-Index", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "ACID-Transactions", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-SQL", "feature": "LIMIT-OFFSET-Pagination", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
        {"vendor": "AWS", "api": "RDS-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "RDS-Document", "feature": "JSON-Ops", "status": "GA", "added_date": "2016-04-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.FeatureSupport.html"},
        {"vendor": "AWS", "api": "RDS-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "RDS-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2009-10-01", "doc_url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"},
    ]
    
    # DocumentDB
    documentdb_features = [
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "find", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "insert", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "update", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "delete", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "aggregate", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "Index-Creation", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "Cursor-Pagination", "status": "GA", "added_date": "2019-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/"},
        {"vendor": "AWS", "api": "DocumentDB-Document", "feature": "ACID-Transactions", "status": "GA", "added_date": "2020-05-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/transactions.html"},
        {"vendor": "AWS", "api": "DocumentDB-SQL", "feature": "SQL-Query", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "DocumentDB-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "DocumentDB-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "DocumentDB-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2020-01-01", "doc_url": "https://docs.aws.amazon.com/documentdb/latest/developerguide/text-search.html"},
    ]
    
    # Neptune (Graph)
    neptune_features = [
        {"vendor": "AWS", "api": "Neptune-Graph", "feature": "Gremlin-Traversal", "status": "GA", "added_date": "2018-05-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/"},
        {"vendor": "AWS", "api": "Neptune-Graph", "feature": "SPARQL-Query", "status": "GA", "added_date": "2018-05-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/"},
        {"vendor": "AWS", "api": "Neptune-Graph", "feature": "openCypher-Query", "status": "GA", "added_date": "2020-07-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-opencypher.html"},
        {"vendor": "AWS", "api": "Neptune-Graph", "feature": "Graph-Indexing", "status": "GA", "added_date": "2018-05-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/"},
        {"vendor": "AWS", "api": "Neptune-Graph", "feature": "ACID-Transactions", "status": "GA", "added_date": "2018-05-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/"},
        {"vendor": "AWS", "api": "Neptune-SQL", "feature": "SQL-Query", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "Neptune-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "Neptune-Document", "feature": "Document-Storage", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "Neptune-Search", "feature": "Full-Text-Search", "status": "Preview", "added_date": "2024-01-01", "doc_url": "https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-text-search.html"},
    ]
    
    # OpenSearch
    opensearch_features = [
        {"vendor": "AWS", "api": "OpenSearch-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2021-09-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/"},
        {"vendor": "AWS", "api": "OpenSearch-Search", "feature": "Vector-Search", "status": "GA", "added_date": "2023-01-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html"},
        {"vendor": "AWS", "api": "OpenSearch-Search", "feature": "Aggregations", "status": "GA", "added_date": "2021-09-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/"},
        {"vendor": "AWS", "api": "OpenSearch-Document", "feature": "Document-Storage", "status": "GA", "added_date": "2021-09-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/"},
        {"vendor": "AWS", "api": "OpenSearch-Search", "feature": "Cursor-Pagination", "status": "GA", "added_date": "2021-09-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/"},
        {"vendor": "AWS", "api": "OpenSearch-SQL", "feature": "SQL-Query", "status": "GA", "added_date": "2021-09-01", "doc_url": "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sql-support.html"},
        {"vendor": "AWS", "api": "OpenSearch-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "AWS", "api": "OpenSearch-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
    ]
    
    data.extend(dynamodb_features)
    data.extend(rds_features)
    data.extend(documentdb_features)
    data.extend(neptune_features)
    data.extend(opensearch_features)
    
    return data

def collect_gcp_data() -> List[Dict[str, Any]]:
    """Collect Google Cloud Platform database service API coverage data"""
    data = []
    
    # Cloud Firestore
    firestore_features = [
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "get", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "set", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "update", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "delete", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "Collection-Query", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "Composite-Index", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "Cursor-Pagination", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Document", "feature": "ACID-Transactions", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-SQL", "feature": "SQL-Query", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "Firestore-KV", "feature": "Key-Value-Access", "status": "GA", "added_date": "2017-10-01", "doc_url": "https://cloud.google.com/firestore/docs"},
        {"vendor": "GCP", "api": "Firestore-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "Firestore-Search", "feature": "Full-Text-Search", "status": "Preview", "added_date": "2024-01-01", "doc_url": "https://cloud.google.com/firestore/docs/vector-search"},
    ]
    
    # Cloud SQL
    cloudsql_features = [
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "SELECT", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "INSERT", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "UPDATE", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "DELETE", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "B-Tree-Index", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "ACID-Transactions", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-SQL", "feature": "LIMIT-OFFSET-Pagination", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
        {"vendor": "GCP", "api": "CloudSQL-Document", "feature": "JSON-Ops", "status": "GA", "added_date": "2020-01-01", "doc_url": "https://cloud.google.com/sql/docs/postgres/json"},
        {"vendor": "GCP", "api": "CloudSQL-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "CloudSQL-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "CloudSQL-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2011-10-01", "doc_url": "https://cloud.google.com/sql/docs"},
    ]
    
    # Bigtable  
    bigtable_features = [
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Get", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Put", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Delete", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Scan", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Column-Family-Index", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-KV", "feature": "Row-Range-Pagination", "status": "GA", "added_date": "2015-05-01", "doc_url": "https://cloud.google.com/bigtable/docs"},
        {"vendor": "GCP", "api": "Bigtable-SQL", "feature": "SQL-Query", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "Bigtable-Document", "feature": "Document-Storage", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "Bigtable-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "GCP", "api": "Bigtable-Search", "feature": "Full-Text-Search", "status": "NA", "added_date": "", "doc_url": ""},
    ]
    
    data.extend(firestore_features)
    data.extend(cloudsql_features)
    data.extend(bigtable_features)
    
    return data

def collect_azure_data() -> List[Dict[str, Any]]:
    """Collect Microsoft Azure database service API coverage data"""
    data = []
    
    # Cosmos DB
    cosmosdb_features = [
        {"vendor": "Azure", "api": "CosmosDB-SQL", "feature": "SELECT", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-SQL", "feature": "INSERT", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-SQL", "feature": "UPDATE", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-SQL", "feature": "DELETE", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Document", "feature": "Document-CRUD", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-KV", "feature": "Key-Value-Access", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Graph", "feature": "Gremlin-Traversal", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Graph", "feature": "Graph-Indexing", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Document", "feature": "Composite-Index", "status": "GA", "added_date": "2018-01-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Document", "feature": "Continuation-Token-Pagination", "status": "GA", "added_date": "2017-05-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Document", "feature": "ACID-Transactions", "status": "GA", "added_date": "2018-11-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
        {"vendor": "Azure", "api": "CosmosDB-Search", "feature": "Full-Text-Search", "status": "Preview", "added_date": "2023-01-01", "doc_url": "https://docs.microsoft.com/azure/cosmos-db/"},
    ]
    
    # SQL Database
    sqldb_features = [
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "SELECT", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "INSERT", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "UPDATE", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "DELETE", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "B-Tree-Index", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "ACID-Transactions", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-SQL", "feature": "OFFSET-FETCH-Pagination", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-Document", "feature": "JSON-Ops", "status": "GA", "added_date": "2016-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-Graph", "feature": "Graph-Tables", "status": "GA", "added_date": "2017-11-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2010-01-01", "doc_url": "https://docs.microsoft.com/azure/azure-sql/"},
        {"vendor": "Azure", "api": "SQLDatabase-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
    ]
    
    data.extend(cosmosdb_features)
    data.extend(sqldb_features)
    
    return data

def collect_mongodb_data() -> List[Dict[str, Any]]:
    """Collect MongoDB database service API coverage data"""
    data = []
    
    mongodb_features = [
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "find", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "insertOne", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "updateOne", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "deleteOne", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "aggregate", "status": "GA", "added_date": "2012-03-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "Index-Creation", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "Cursor-Pagination", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Document", "feature": "ACID-Transactions", "status": "GA", "added_date": "2018-06-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-SQL", "feature": "SQL-Query", "status": "GA", "added_date": "2020-10-01", "doc_url": "https://docs.mongodb.com/compass/master/query/sql/"},
        {"vendor": "MongoDB", "api": "MongoDB-Search", "feature": "Atlas-Search", "status": "GA", "added_date": "2020-06-01", "doc_url": "https://docs.atlas.mongodb.com/atlas-search/"},
        {"vendor": "MongoDB", "api": "MongoDB-Search", "feature": "Vector-Search", "status": "GA", "added_date": "2023-06-01", "doc_url": "https://docs.atlas.mongodb.com/atlas-vector-search/"},
        {"vendor": "MongoDB", "api": "MongoDB-KV", "feature": "Key-Value-Access", "status": "GA", "added_date": "2009-02-01", "doc_url": "https://docs.mongodb.com/"},
        {"vendor": "MongoDB", "api": "MongoDB-Graph", "feature": "Graph-Lookup", "status": "GA", "added_date": "2016-11-01", "doc_url": "https://docs.mongodb.com/"},
    ]
    
    data.extend(mongodb_features)
    return data

def collect_datastax_data() -> List[Dict[str, Any]]:
    """Collect DataStax database service API coverage data"""
    data = []
    
    datastax_features = [
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "GET", "status": "GA", "added_date": "2010-07-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "PUT", "status": "GA", "added_date": "2010-07-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "DELETE", "status": "GA", "added_date": "2010-07-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-SQL", "feature": "CQL-SELECT", "status": "GA", "added_date": "2011-08-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-SQL", "feature": "CQL-INSERT", "status": "GA", "added_date": "2011-08-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-SQL", "feature": "CQL-UPDATE", "status": "GA", "added_date": "2011-08-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-SQL", "feature": "CQL-DELETE", "status": "GA", "added_date": "2011-08-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-Document", "feature": "JSON-Support", "status": "GA", "added_date": "2014-09-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "Secondary-Index", "status": "GA", "added_date": "2012-01-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "Token-Based-Pagination", "status": "GA", "added_date": "2010-07-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Cassandra-KV", "feature": "Lightweight-Transactions", "status": "GA", "added_date": "2013-12-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Astra-Document", "feature": "Document-API", "status": "GA", "added_date": "2020-07-01", "doc_url": "https://docs.datastax.com/en/astra-serverless/docs/"},
        {"vendor": "DataStax", "api": "Astra-Document", "feature": "JSON-API", "status": "GA", "added_date": "2023-11-01", "doc_url": "https://docs.datastax.com/en/astra-db-serverless/api-reference/json-api.html"},
        {"vendor": "DataStax", "api": "Cassandra-Graph", "feature": "Graph-Traversal", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "DataStax", "api": "Cassandra-Search", "feature": "Search-Index", "status": "GA", "added_date": "2015-04-01", "doc_url": "https://docs.datastax.com/"},
        {"vendor": "DataStax", "api": "Astra-Search", "feature": "Vector-Search", "status": "GA", "added_date": "2023-08-01", "doc_url": "https://docs.datastax.com/en/astra-db-serverless/api-reference/"},
    ]
    
    data.extend(datastax_features)
    return data

def collect_neo4j_data() -> List[Dict[str, Any]]:
    """Collect Neo4j database service API coverage data"""
    data = []
    
    neo4j_features = [
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Cypher-MATCH", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Cypher-CREATE", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Cypher-MERGE", "status": "GA", "added_date": "2013-04-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Cypher-DELETE", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Graph-Indexing", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "Cursor-Pagination", "status": "GA", "added_date": "2018-05-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "ACID-Transactions", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Graph", "feature": "GQL-Standard", "status": "Preview", "added_date": "2024-01-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Search", "feature": "Full-Text-Search", "status": "GA", "added_date": "2016-04-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-Search", "feature": "Vector-Search", "status": "GA", "added_date": "2023-08-01", "doc_url": "https://neo4j.com/docs/"},
        {"vendor": "Neo4j", "api": "Neo4j-SQL", "feature": "SQL-Query", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "Neo4j", "api": "Neo4j-KV", "feature": "Key-Value-Access", "status": "NA", "added_date": "", "doc_url": ""},
        {"vendor": "Neo4j", "api": "Neo4j-Document", "feature": "Document-Storage", "status": "GA", "added_date": "2010-02-01", "doc_url": "https://neo4j.com/docs/"},
    ]
    
    data.extend(neo4j_features)
    return data

def main():
    """Main data collection function"""
    all_data = []
    
    print("Collecting AWS data...")
    all_data.extend(collect_aws_data())
    
    print("Collecting GCP data...")
    all_data.extend(collect_gcp_data())
    
    print("Collecting Azure data...")
    all_data.extend(collect_azure_data())
    
    print("Collecting MongoDB data...")
    all_data.extend(collect_mongodb_data())
    
    print("Collecting DataStax data...")
    all_data.extend(collect_datastax_data())
    
    print("Collecting Neo4j data...")
    all_data.extend(collect_neo4j_data())
    
    # Sort by vendor, then API, then feature
    all_data.sort(key=lambda x: (x['vendor'], x['api'], x['feature']))
    
    # Write to CSV
    filename = f"2025-08-20__data__api-coverage-parity__multi-vendor__feature-matrix.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['vendor', 'api', 'feature', 'status', 'added_date', 'doc_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in all_data:
            writer.writerow(row)
    
    print(f"Collected {len(all_data)} API capability records")
    print(f"Data saved to: {filename}")
    
    # Generate summary statistics
    vendors = set(row['vendor'] for row in all_data)
    apis = set(row['api'] for row in all_data)
    statuses = set(row['status'] for row in all_data)
    
    print(f"\nSummary:")
    print(f"- Vendors: {len(vendors)} ({', '.join(sorted(vendors))})")
    print(f"- APIs: {len(apis)}")
    print(f"- Status types: {', '.join(sorted(statuses))}")
    
    # Status breakdown
    status_counts = {}
    for row in all_data:
        status = row['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\nStatus Distribution:")
    for status, count in sorted(status_counts.items()):
        print(f"- {status}: {count} features")

if __name__ == "__main__":
    main()