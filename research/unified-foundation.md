---
layout: default
title: "The Shift Towards a Unified Foundation"
permalink: /research/unified-foundation/
---

# The Shift Towards a Unified Foundation

**Prepared by:** Patrick McFadin

## Abstract

The data management landscape is undergoing a paradigm shift, moving decisively away from fragmented, database-centric architectures toward a unified, storage-centric model. This new paradigm is characterized by three core trends: the decoupling of compute and storage, the standardization of data access interfaces and formats, and the consolidation of specialized database features into multi-model platforms. Object storage, with the Amazon S3 API as its lingua franca, has become the foundational layer for modern analytics, enabling a flexible and cost-effective multi-engine ecosystem. Open table formats like Apache Iceberg are accelerating this transition by bringing ACID transactions, schema evolution, and engine interoperability to the data lake. Concurrently, database systems are converging, with multi-model engines absorbing specialized capabilities and query languages standardizing around common, portable syntax like ISO GQL and IETF JSONPath. This paper analyzes the technological drivers and strategic implications of this shift, arguing that the storage-centric stack is prevailing due to its superior economics, reduced vendor lock-in, and greater architectural agility. While challenges related to performance at extreme scale and ecosystem maturity persist, the trajectory is clear: the future of data architecture is modular, open, and built upon a durable, independent storage foundation.

## Introduction: From Polyglot Persistence to a Unified Foundation

For the past two decades, the dominant philosophy in data architecture has been "polyglot persistence"—the practice of using a menagerie of specialized databases, each selected for its unique ability to handle a specific data model or workload. An organization's data ecosystem was a patchwork quilt of relational databases for transactions, document stores for flexible schemas, graph databases for connected data, and columnar warehouses for analytics. This "right tool for the job" approach delivered optimized performance for individual tasks but came at the steep price of operational complexity. Each new database introduced its own query language, scaling strategy, and maintenance overhead, creating data silos and requiring specialized expertise that was difficult to scale.

Today, the pendulum is swinging back from fragmentation toward consolidation. A new architectural paradigm is emerging, one that inverts the traditional model. Instead of data being captive within dozens of disparate database engines, a flexible and durable storage layer is becoming the central, foundational platform. This **storage-centric stack**—built on open standards, decoupled components, and interoperable engines—is rapidly becoming the default for modern data platforms.

This transformation is not a single trend but a confluence of mutually reinforcing developments. At the lowest level, object storage has become the universal substrate for data, standardized around the Amazon S3 API. Atop this foundation, open table formats like Apache Iceberg are imposing structure and reliability, turning data lakes into true data warehouses. Above this, query engines and database platforms are undergoing their own consolidation. Multi-model databases are absorbing the functionalities of their specialized predecessors, while query languages are homogenizing around common standards, eroding the vendor-specific dialects that once defined the landscape.

This paper will examine this paradigm shift in detail, arguing that the storage-centric model is outcompeting the database-centric model on the key dimensions of cost, flexibility, and strategic resilience. We will dissect the foundational role of object storage and open table formats, analyze the convergence of database access patterns and query languages, and explore the profound economic and strategic implications of decoupling compute from storage. While acknowledging the scenarios where specialized systems persist, the evidence overwhelmingly indicates a fundamental re-architecting of the data ecosystem around a shared, open, and durable storage core.

---

## Section 1: The Storage-Centric Stack: S3 and Parquet as the New Foundation

The bedrock of the modern data stack is no longer the database engine but the storage layer itself. Specifically, cloud object storage, with the Amazon S3 API as its de facto standard, has become the universal "data operating system." This shift is redefining where data lives and how it is accessed, making direct queries on open file formats like Parquet the new norm for analytical workloads. This foundational change favors flexibility and interoperability over the monolithic, closed systems of the past.

### The S3 API as the Lingua Franca of Data

The Amazon S3 API has transcended its origins to become the industry's lingua franca for large-scale data storage. Its widespread adoption by all major cloud providers and on-premises vendors has created a standardized interface that applications can target, regardless of the underlying storage provider. This standardization is a powerful enabler of portability and multi-cloud strategies. An application written to use the S3 API can seamlessly switch its backend from AWS S3 to Google Cloud Storage, an on-premises MinIO cluster, or a competing cloud storage provider, often with only a configuration change.

This near-universal compatibility mitigates vendor lock-in and has fostered a rich ecosystem of tools—from backup software to machine learning frameworks—that assume the existence of an S3-compatible endpoint. The result is that organizations can now build cloud-agnostic data architectures, a critical advantage in an era of intense competition among cloud providers.

### Direct Querying on Object Storage Becomes the Default

Hand-in-hand with S3 standardization is the rise of direct querying on data stored in open formats like Parquet and ORC. Instead of enduring a costly and time-consuming Extract, Transform, Load (ETL) process to move data into a proprietary warehouse, organizations are increasingly leaving the data in place and querying it directly with powerful SQL engines.

This "lakehouse" architecture is no longer a niche practice but a mainstream approach. A 2024 industry survey revealed that 65% of IT and data professionals now run over half of their analytics workloads on a data lakehouse. The sheer scale of this trend is staggering; in 2024 alone, Amazon Redshift users scanned over 77 exabytes of data directly from S3, demonstrating that querying data "in situ" is a cornerstone of modern analytics. Leading cloud data warehouses, including Snowflake and Google BigQuery, have all embraced this model by enabling external tables and query federation to data in object storage. This approach offers compelling benefits: it eliminates data movement and duplication, unifies data access for diverse tools, and, most importantly, allows for the independent scaling of compute and storage, leading to significant cost efficiencies.

### Persistent Limitations and Nuances

Despite its ascendancy, the storage-centric foundation is not without its challenges. Full interoperability remains a work in progress. While the core S3 API is standardized, vendor implementations can vary in their support for advanced features and extensions, leading to minor incompatibilities. More significantly, the practical "lift-and-shift" of workloads between clouds is often hindered not by technical barriers but by the prohibitive cost and time required to move petabytes of data across the internet.

Furthermore, direct querying on object storage has yet to achieve performance parity with traditional warehouses for all workloads. Specialized engines still tend to outperform lakehouse query engines for concurrent, low-latency BI queries that power interactive dashboards. This performance gap leads many organizations to adopt a two-tier architecture, using the data lake for raw data and ETL, while maintaining a curated data warehouse for high-performance business intelligence. The promise of a single, unified platform has not yet been fully realized for every use case.

---

## Section 2: Unifying Access Patterns: The Rise of Multi-Model Databases

As the storage layer standardizes, a parallel consolidation is occurring at the database level. The era of rampant specialization—"polyglot persistence"—is giving way to the rise of powerful, multi-model databases. These general-purpose engines are increasingly absorbing the capabilities of their niche predecessors, aiming to handle diverse data models like relational, document, graph, and key-value within a single, unified platform. This trend is driven by user demand for simpler architectures, lower costs, and the accelerated pace of development in the cloud.

### Absorbing Specialized Functions into the Core

The most significant trend is the absorption of specialized functionalities as features within mainstream database engines. Not long ago, workloads involving time-series data or vector similarity search required dedicated, purpose-built databases like InfluxDB or Pinecone. Today, this functionality is rapidly becoming a standard feature of generalist platforms. PostgreSQL, for example, can be transformed into a highly performant time-series database with the TimescaleDB extension and a competitive vector database with `pgvector`. Similarly, MongoDB Atlas and Redis have integrated robust vector search capabilities, allowing developers to leverage these features within a familiar ecosystem.

This consolidation is proving to be "good enough" for a vast number of use cases, effectively narrowing the performance gap that once justified the operational overhead of a specialized engine. A recent industry survey highlighted this preference, showing that developers were more than twice as likely to use PostgreSQL or MongoDB for vector workloads than specialized alternatives. The forecast is clear: by 2026, the majority of new database systems are expected to be multi-model by design, reducing the need for a separate database for every use case.

### Cloud Vendors Accelerate Convergence Through API Compatibility

This shift is being heavily accelerated by cloud providers, who are increasingly marketing their database services based on API compatibility rather than proprietary engine names. Services like Amazon Aurora are explicitly branded as "MySQL- and PostgreSQL-compatible," while Amazon DocumentDB offers "MongoDB compatibility". This strategy lowers adoption friction by allowing organizations to migrate existing applications with minimal code changes, effectively using the open-source API as a gateway to a more scalable, cloud-native backend.

This focus on interfaces over engines is changing how databases are procured and deployed. Instead of mandating a specific product, decision-makers now specify a required interface, such as "PostgreSQL-compatible" or "Redis-compatible". Platforms like Azure Cosmos DB take this to its logical conclusion, offering a single backend service that exposes multiple popular APIs—SQL, MongoDB, Cassandra, and Gremlin—allowing different development teams to use their preferred tools against a unified data store. These multi-API gateways and compatible services are fundamentally undermining the rationale for bespoke, single-interface systems.

### The Enduring Role of the Specialist

However, the push for consolidation does not spell the absolute end of specialized databases. For workloads at the extreme end of the performance or scale spectrum, purpose-built systems often retain a significant advantage. A high-frequency trading system may still rely on a specialized in-memory database to achieve microsecond latencies that a generalist engine cannot match. Similarly, for deep, complex graph traversals, the developer experience and specialized query language of an engine like Neo4j can offer productivity gains that a multi-model database's graph features cannot replicate.

Moreover, the "one-size-fits-all" approach carries the risk of creating a system that is a jack-of-all-trades but master of none, potentially "not being really good at anything". This viewpoint is championed by vendors like Amazon, which continues to advocate for a portfolio of "purpose-built databases" to avoid the compromises inherent in converged systems. This strategic divergence ensures that while multi-model databases will capture the mainstream, a healthy ecosystem of specialized solutions will persist for the demanding niches that require them.

---

## Section 3: Interoperability Layers: Homogenizing the Query Experience

Above the storage and database layers, a powerful trend toward homogenization is reshaping the user and developer experience. The fragmented landscape of vendor-specific query dialects is steadily giving way to a more unified environment built on common standards and interoperable query engines. This convergence, driven by new SQL standards, the rise of federated query engines, and industry-wide collaboration on new languages like ISO GQL, is dramatically improving query portability and reducing vendor lock-in.

### The Convergence of SQL and NoSQL on Common Standards

For years, a chasm existed between the structured world of SQL and the flexible-schema world of NoSQL. That gap has narrowed significantly as both sides have converged on common standards for handling semi-structured data. All major relational databases, including PostgreSQL and MySQL, have added robust, native support for JSON, adhering to the SQL/JSON standard. Simultaneously, the 2024 publication of the IETF's JSONPath standard (RFC 9535) is creating a single, language-independent syntax for querying JSON documents, aiming to eliminate the inconsistencies that have plagued different implementations for years.

This convergence means developers no longer face a stark choice between relational and document models. They can now store and query schemaless JSON data efficiently within a traditional SQL database, using standard query syntax that is increasingly portable across platforms. This trend extends even to search engines like Elasticsearch and OpenSearch, which now offer SQL interfaces, further cementing SQL's role as the universal "query glue" for a wide range of data stores.

### The Unification of Graph and the Evolution of SQL

The move toward standardization is also transforming newer database categories. The graph database market, long fragmented by competing languages like Cypher, Gremlin, and PGQL, is poised for unification with the 2024 publication of ISO GQL (Graph Query Language). Developed with broad industry support, GQL has been embraced by leading vendors like Neo4j, TigerGraph, and AWS, who have all committed to aligning their platforms with the new standard. This consensus promises to dramatically improve query portability and create a unified ecosystem for graph analytics, mirroring the role SQL plays for relational data.

At the same time, the SQL standard itself continues to evolve, absorbing features that were once proprietary vendor extensions. The latest standard, SQL:2023, codified many common functions and introduced property graph queries (SQL/PGQ) directly into the SQL language. This continuous process of standardization steadily shrinks the surface area of vendor-specific syntax, making it easier for developers to write portable queries that are not locked into a single ecosystem.

### Persistent Dialects and the Limits of Convergence

Despite this clear trend toward homogenization, significant variations persist. The most glaring exception is in procedural SQL. The languages used for stored procedures—Oracle's PL/SQL, Microsoft's T-SQL, and PostgreSQL's PL/pgSQL—remain deeply incompatible, with little evidence of convergence. Migrating logic written in these dialects requires substantial and costly rewriting, creating a powerful form of lock-in for legacy applications.

Furthermore, vendors, particularly in the cloud data warehousing space, continue to introduce powerful but proprietary extensions for specialized workloads like machine learning, geospatial analysis, and semi-structured data processing. A query that leverages Google BigQuery's `ML.PREDICT` functions or Snowflake's `FLATTEN` command will not run on any other platform. Finally, the adoption of new standards like GQL and JSONPath is still in its early stages. As of 2025, many existing applications still rely on older languages like Gremlin, and full implementation of the new standards across all major databases will take time. While the long-term trajectory is toward unification, complete query portability has not yet been achieved.

---

## Section 4: The Role of Apache Iceberg: A Cornerstone of the New Stack

Perhaps no single technology better exemplifies the principles of the storage-centric stack than Apache Iceberg. As an open table format, Iceberg acts as a critical abstraction layer that decouples data tables from both the underlying file storage and the overlying compute engines. It brings structure, reliability, and robust data management features to vast pools of data in object stores, effectively bridging the gap between the raw, untamed data lake and the curated, transactional data warehouse.

### Enabling a True Multi-Engine Ecosystem

At its core, Iceberg is designed to be engine-agnostic. A table defined in Iceberg format on S3 is not tied to any single processing framework; it can be read and written consistently by a diverse and growing ecosystem of engines, including Spark, Trino, Flink, and Snowflake. This interoperability is the key to breaking down the data silos created by traditional databases. An organization can use Spark for large-scale batch ETL, Flink for real-time stream processing, and Trino for ad-hoc interactive SQL queries—all operating on the exact same physical data without conflict or data movement.

This capability makes engine swaps and pilots dramatically simpler. A team can test a new query engine on its existing data with virtually no upfront data migration, a stark contrast to the past where such an evaluation would require a massive ETL project. This flexibility gives organizations immense bargaining power and the agility to adopt the best compute technology for a given task without being constrained by past storage decisions.

### Bringing ACID Transactions and Warehouse Features to the Lake

Before the advent of table formats, data lakes were notoriously unreliable. Lacking transactional guarantees, concurrent operations could easily lead to corrupted data, and failed jobs often left datasets in an inconsistent state. Iceberg solves these problems by providing ACID transaction guarantees for operations on object storage. It manages table state through atomic metadata pointers, ensuring that readers always see a consistent snapshot of the data and that operations are serializable.

Beyond transactions, Iceberg introduces a suite of features once exclusive to data warehouses directly to the data lake. These include:

- **Schema Evolution:** Iceberg allows for the safe addition, deletion, renaming, and reordering of columns without rewriting table data, preventing downstream data pipelines from breaking.
- **Hidden Partitioning:** It can automatically manage partition values based on table data (e.g., partitioning by month from a timestamp column), freeing users from having to include partition columns in their queries.
- **Time Travel and Versioning:** Iceberg maintains a history of table snapshots, allowing users to query previous versions of a table for historical analysis, reproducibility, or disaster recovery.

### The Path to Becoming the De Facto Standard

Iceberg is rapidly gaining momentum and is on a clear trajectory to become the de facto standard for open analytic table storage. Its development was initiated at Netflix and it benefits from a vibrant, community-driven ecosystem, which appeals to neutral parties like AWS and Google. This widespread backing from nearly every major data platform vendor—including former competitors like Snowflake and Databricks—signals a powerful industry consensus.

However, adoption is still in its early stages. Analysts place Iceberg at the "peak of inflated expectations" on the technology hype cycle, indicating that while enthusiasm is high, widespread production deployment is still ramping up. Organizations must still navigate the "table format wars" between Iceberg, Delta Lake, and Hudi, and the tooling ecosystem around these formats is less mature than that of traditional warehouses. For now, many enterprises are piloting Iceberg or using it in a hybrid model, retaining their warehouses for mission-critical BI workloads that demand maximum performance and stability. Despite these caveats, Iceberg stands as a cornerstone technology, making the vision of a flexible, open, and powerful storage-centric stack a practical reality.

---

## Section 5: Economic and Strategic Implications: Lowering TCO and Reducing Lock-in

The architectural shift toward a decoupled, storage-centric stack is not merely a technical evolution; it is fundamentally driven by powerful economic and strategic incentives. Organizations are embracing this new model primarily to achieve a dramatically lower Total Cost of Ownership (TCO) and to escape the vendor lock-in that has long plagued the database market. This paradigm shift enables a more flexible and resilient approach to data infrastructure, where technology choices are dictated by value and performance rather than by historical commitments.

### The Economic Case: Drastically Lowering Total Cost of Ownership

The most compelling driver for adopting a storage-centric architecture is its superior economics, particularly at scale. By separating compute from storage, organizations can optimize spending on each dimension independently. Data can be stored cheaply and durably in commodity object storage, while compute resources are provisioned elastically, scaling up only when work needs to be done and scaling down to zero to avoid idle costs. This stands in stark contrast to the bundled pricing of traditional data warehouses, where organizations often pay a premium for storage and are forced to scale expensive compute nodes just to accommodate data growth.

The financial impact is significant. A 2024 survey found that 56% of organizations adopting a lakehouse architecture expected cost savings of over 50%, with nearly a third of large enterprises anticipating savings greater than 75%. These figures are substantiated by high-profile case studies of companies like 37signals, Twitter (X), and Ahrefs, which have reported savings of 60% or more by repatriating workloads from cloud warehouses to private, storage-centric infrastructure. These savings stem from the lower cost of object storage, the avoidance of expensive licensing fees, and the elimination of redundant data copies that proliferate in warehouse-centric environments.

### The Strategic Case: Escaping Vendor Lock-In

Beyond cost, the storage-centric model offers a powerful strategic advantage: freedom from vendor lock-in. In a traditional architecture, data is stored in a vendor's proprietary format, accessible only through their proprietary engine. Migrating to a new platform is a monumental undertaking, requiring a complete data export and rewrite of application logic. This creates immense friction and gives incumbent vendors significant pricing power.

The new stack systematically dismantles this lock-in at every layer:

- **Storage Layer:** Standardizing on the S3 API ensures that the storage backend can be swapped with minimal disruption.
- **Data Layer:** Open table formats like Iceberg ensure that the structured data itself is not tied to any single query engine.
- **Query Layer:** The homogenization of SQL and the rise of API compatibility means that queries and application code are more portable than ever before.
- **Application Layer:** API gateways like DataStax Stargate and multi-API databases like Azure Cosmos DB allow developers to use common, open APIs (like GraphQL or MongoDB's API) against different backends, further decoupling the application from the database.

This multi-layered interoperability is fundamentally changing procurement practices. Organizations are increasingly specifying requirements in terms of standard interfaces (e.g., "must be PostgreSQL-compatible") rather than specific vendor products. This forces vendors to compete on performance, features, and cost, rather than on the stickiness of a proprietary ecosystem.

### Navigating the Trade-Offs

The benefits of lower TCO and reduced lock-in are not without trade-offs. A decoupled, "best-of-breed" stack can introduce greater operational complexity than a single, fully-managed warehouse solution. Engineering teams must take on the responsibility of integrating, managing, and securing multiple components, and the potential for a poorly governed "data swamp" can negate infrastructure savings with lost productivity. Furthermore, while multi-cloud portability is technically feasible, the high egress fees charged by cloud providers can make large-scale data migration economically impractical, creating a form of de facto data gravity. Nevertheless, for a growing number of organizations, the immense cost savings and strategic flexibility offered by the storage-centric model far outweigh these challenges, establishing it as the definitive direction for the future of data architecture.

---

## Conclusion

The data infrastructure landscape is in the midst of a foundational realignment. The evidence presented paints a clear picture of an industry moving with conviction from a fragmented, database-centric past to an integrated, storage-centric future. This new paradigm, built on the principles of decoupling, standardization, and consolidation, promises a more flexible, cost-effective, and resilient approach to data management.

The shift begins at the bottom of the stack, where the S3 API and open file formats have established object storage as the durable and universal foundation for data. Atop this layer, open table formats like Apache Iceberg are providing the transactional integrity and rich metadata necessary to transform data lakes into the primary systems for modern analytics. This architecture has, in turn, fueled the rise of a vibrant multi-engine ecosystem, liberating data from the silos of proprietary databases and allowing organizations to apply the best compute tool for any given task.

This decoupling of compute from storage, combined with the convergence of query languages and the rise of multi-model databases, is systematically dismantling the vendor lock-in that has long constrained the industry. The resulting improvements in portability and interoperability are empowering organizations to build architectures that are not only more agile but also dramatically more cost-efficient.

While the transition is not yet complete—and specialized databases will continue to play a vital role for niche, high-performance workloads—the trajectory is undeniable. The future of data architecture is one where storage is the stable, central platform and compute is an elastic, interchangeable commodity. The era of building data platforms around a constellation of siloed, monolithic databases is fading. In its place is rising a more logical and sustainable model: a unified storage core, accessed through standard interfaces, and capable of serving a diverse and evolving set of analytical and operational workloads.

---

## Executive Summary

The modern data architecture is undergoing a fundamental paradigm shift, moving from a complex, "database-centric" model to a unified and efficient "storage-centric" model. This transformation is driven by the need for greater flexibility, lower total cost of ownership (TCO), and freedom from vendor lock-in. This paper analyzes the key technological trends and strategic implications of this new architectural paradigm.

### Key Findings:

1. **The Foundation is Shifting to Object Storage:** Cloud object storage, standardized around the Amazon S3 API, has become the de facto foundational layer for data. An increasing majority of analytical queries are now executed directly on open file formats (like Parquet) residing in object storage, bypassing traditional data warehouses. This "lakehouse" approach eliminates costly data movement and allows for the independent, cost-effective scaling of storage and compute resources.

2. **Multi-Model Databases are Consolidating the Landscape:** The era of "polyglot persistence," which required a separate specialized database for each data model, is ending. Multi-model, general-purpose databases are becoming mainstream by absorbing specialized functionalities like time-series, graph, and vector search as core features. This consolidation is accelerated by cloud vendors who prioritize API compatibility (e.g., "PostgreSQL-compatible"), simplifying architecture and reducing operational overhead.

3. **Query Languages and Interfaces are Homogenizing:** Vendor-specific query dialects are receding in favor of common standards that enhance portability. The convergence of SQL and NoSQL databases on standards like SQL/JSON and IETF JSONPath, coupled with the industry-wide alignment on the new ISO GQL for graph databases, is creating a more unified and interoperable query experience. While some proprietary extensions and incompatible procedural languages persist, the trend is overwhelmingly toward standardization.

4. **Apache Iceberg is a Cornerstone Technology:** The open table format Apache Iceberg exemplifies and accelerates the shift to a storage-centric stack. By bringing ACID transactions, schema evolution, and other warehouse-like features to data lakes, Iceberg enables a true multi-engine ecosystem where tools like Spark, Trino, and Snowflake can operate on the same data. This decouples data from compute, breaking down silos and enabling unprecedented architectural agility.

5. **The Shift is Driven by Economics and Strategy:** The primary motivators for this paradigm shift are a significantly lower TCO and the strategic imperative to reduce vendor lock-in. Industry surveys and case studies show that storage-centric architectures can reduce analytics costs by 50% or more by leveraging commodity storage and elastic compute. At the same time, standardizing on open APIs and formats at every layer of the stack gives organizations the freedom to choose best-of-breed tools and avoid being trapped in a single vendor's ecosystem.

In conclusion, the storage-centric stack represents a maturing of the data management field. While challenges remain, the industry is coalescing around a more sustainable and powerful model where a durable, independent storage foundation supports a flexible and interchangeable set of compute engines. This shift is poised to define the next decade of data architecture, prioritizing openness, efficiency, and agility.

---

*[Download full paper as PDF](/assets/papers/the-shift-towards-a-unified-foundation.pdf)*

*[Back to Research Papers](/research/)*