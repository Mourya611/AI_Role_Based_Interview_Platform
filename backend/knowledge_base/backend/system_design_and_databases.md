# Backend Architecture, System Design & Databases

## Monolithic vs Microservices Architecture
A monolithic architecture packages all business modules, APIs, and data access layers into a single deployable unit. It provides initial simplicity, single-codebase deployment, and zero network latency between components. However, as team size and codebase scale grow, monoliths suffer from tight coupling, long build times, single points of failure, and rigid technology stacks.

Microservices architecture decomposes applications into small, independently deployable services organized around business capabilities. Services communicate over lightweight protocols like HTTP/REST or gRPC. Key advantages include fault isolation, independent scaling, and tech-stack flexibility. Trade-offs include distributed system complexity, event network latency, eventual consistency challenges, and complex monitoring/tracing requirements.

## Database Indexing & Query Optimization
Database indexing uses B-Tree or Hash data structures to optimize lookup queries. A B-Tree index maintains sorted key pointers, reducing search complexity from O(N) full table scans to O(log N). Composite indexes optimize multi-column queries but require matching the leftmost prefix rule.

Over-indexing degrades write performance because INSERT, UPDATE, and DELETE operations must synchronously update index structures. To optimize slow PostgreSQL queries:
1. Run EXPLAIN ANALYZE to identify sequential scans, hash joins, or high cost steps.
2. Add targeted B-Tree or GIN/GiST indexes.
3. Eliminate SELECT * and fetch only required columns.
4. Avoid functions on indexed columns in WHERE clauses.

## REST vs GraphQL APIs
REST (Representational State Transfer) is a stateless resource-based architectural style using standard HTTP methods (GET, POST, PUT, DELETE). It leverages HTTP caching and standard status codes. Over-fetching and under-fetching occur when endpoints return fixed data structures.

GraphQL provides a typed query language enabling clients to request exact fields across nested resources in a single request. It solves over-fetching and allows client-driven data fetching. Trade-offs include query complexity management, difficult HTTP-level caching, and N+1 query performance risks on the server.
