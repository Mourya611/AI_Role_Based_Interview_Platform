# Cloud Engineering & DevOps Architecture

## Containerization vs Virtualization
Virtual Machines (VMs) virtualize hardware using hypervisors (e.g. ESXi, KVM). Each VM runs a full guest operating system, requiring substantial RAM, storage, and boot overhead.

Docker Containers virtualize the operating system kernel. Containers share the host OS kernel while maintaining isolated user spaces, yielding lightweight, sub-second startup times and predictable environment parity across dev and production.

## Infrastructure as Code (IaC) & CI/CD
Infrastructure as Code tools like Terraform and CloudFormation allow declarative provisioning of cloud resources (VPCs, EC2, RDS, IAM). CI/CD pipelines automate testing, building container images, and deploying updates via rolling or blue/green strategies with zero downtime.
