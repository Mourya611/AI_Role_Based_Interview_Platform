# Data Engineering & Streaming Pipelines

## Batch Processing vs Real-time Streaming
Batch processing processes bulk records periodically (e.g. nightly Apache Spark / Hadoop ETL jobs). High throughput, cost-effective for static reporting, but high latency.

Real-time streaming ingests event streams continuously (e.g. Apache Kafka, Apache Flink, AWS Kinesis). Low latency (sub-second), enables real-time alerting and analytics, but requires managing out-of-order events and checkpointing state management.
