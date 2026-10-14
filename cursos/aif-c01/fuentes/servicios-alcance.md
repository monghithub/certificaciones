# Alcance de servicios AWS (AIF-C01)

Listas literales de la guía oficial (versión 1.1, 30 de abril de 2026). Ambas son no exhaustivas y están sujetas a cambios.

## Servicios dentro de alcance (in scope)

- **Fuente:** <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/aif-01-in-scope-services.html>
- **Fecha de consulta:** 2026-10-14

### Analytics

- AWS Data Exchange
- Amazon EMR
- AWS Glue
- AWS Glue DataBrew
- AWS Lake Formation
- Amazon OpenSearch Service
- Amazon Quick
- Amazon Redshift

### Cloud Financial Management

- AWS Budgets
- AWS Cost Explorer

### Compute

- Amazon EC2
- AWS Lambda

### Containers

- Amazon Elastic Container Service (Amazon ECS)
- Amazon Elastic Kubernetes Service (Amazon EKS)

### Database

- Amazon Aurora
- Amazon DocumentDB (with MongoDB compatibility)
- Amazon DynamoDB
- Amazon ElastiCache
- Amazon Neptune
- Amazon RDS

### Developer Tools

- Kiro
- Strands Agents

### Machine Learning

- Amazon Bedrock
- Amazon Bedrock AgentCore
- Amazon Comprehend
- Amazon Lex
- Amazon Nova
- Amazon Personalize
- Amazon Polly
- Amazon Rekognition
- Amazon SageMaker AI
- Amazon SageMaker JumpStart
- Amazon Textract
- Amazon Transcribe
- Amazon Translate
- AWS Transform

### Management and Governance

- AWS CloudTrail
- Amazon CloudWatch
- AWS Config
- AWS Trusted Advisor
- AWS Well-Architected Tool

### Networking and Content Delivery

- Amazon CloudFront
- Amazon VPC

### Security, Identity, and Compliance

- AWS Artifact
- AWS Identity and Access Management (IAM)
- Amazon Inspector
- AWS Key Management Service (AWS KMS)
- Amazon Macie
- AWS Secrets Manager

### Storage

- Amazon S3
- Amazon S3 Glacier

## Servicios fuera de alcance (out of scope)

- **Fuente:** <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/aif-01-out-of-scope-services.html>
- **Fecha de consulta:** 2026-10-14

### Analytics

- AWS Clean Rooms
- Amazon CloudSearch
- Amazon Managed Streaming for Apache Kafka (Amazon MSK)

### Application Integration

- Amazon AppFlow
- Amazon MQ
- Amazon Simple Workflow Service (Amazon SWF)

### Business Applications

- Amazon Chime
- Amazon Pinpoint
- Amazon Simple Email Service (Amazon SES)
- AWS Supply Chain
- AWS Wickr

### Cloud Financial Management

- AWS Application Cost Profiler
- AWS Billing Conductor
- AWS Marketplace

### Compute

- AWS App Runner
- AWS Elastic Beanstalk
- EC2 Image Builder
- Amazon Lightsail

### Containers

- Red Hat OpenShift Service on AWS (ROSA)

### Customer Enablement

- AWS IQ
- AWS Managed Services (AMS)
- AWS re:Post Private
- AWS Support

### Database

- Amazon Keyspaces (for Apache Cassandra)
- Amazon Quantum Ledger Database (Amazon QLDB)
- Amazon Timestream

### Developer Tools

- AWS AppConfig
- AWS Application Composer
- AWS CloudShell
- Amazon CodeCatalyst
- AWS CodeStar
- AWS Fault Injection Service
- AWS X-Ray

### End User Computing

- Amazon AppStream 2.0
- Amazon WorkSpaces
- Amazon WorkSpaces Thin Client
- Amazon WorkSpaces Web

### Frontend Web and Mobile

- AWS Amplify
- AWS Device Farm
- Amazon Location Service

### Internet of Things (IoT)

- AWS IoT Analytics
- AWS IoT Core
- AWS IoT Device Defender
- AWS IoT Device Management
- AWS IoT Events
- AWS IoT FleetWise
- FreeRTOS
- AWS IoT Greengrass
- AWS IoT 1-Click
- AWS IoT RoboRunner
- AWS IoT SiteWise
- AWS IoT TwinMaker

### Machine Learning

- AWS DeepComposer
- AWS HealthImaging
- AWS HealthOmics
- Amazon Monitron
- AWS Panorama

### Management and Governance

- AWS Control Tower
- AWS Health Dashboard
- AWS Launch Wizard
- AWS License Manager
- Amazon Managed Grafana
- Amazon Managed Service for Prometheus
- AWS OpsWorks
- AWS Organizations
- AWS Proton
- AWS Resilience Hub
- AWS Resource Explorer
- AWS Resource Groups
- AWS Systems Manager Incident Manager
- AWS Service Catalog
- Service Quotas
- AWS Telco Network Builder
- AWS User Notifications

### Media

- Amazon Elastic Transcoder
- AWS Elemental MediaConnect
- AWS Elemental MediaConvert
- AWS Elemental MediaLive
- AWS Elemental MediaPackage
- AWS Elemental MediaStore
- AWS Elemental MediaTailor
- Amazon Interactive Video Service (Amazon IVS)
- Amazon Nimble Studio

### Migration and Transfer

- AWS Application Discovery Service
- AWS Application Migration Service
- AWS Database Migration Service (AWS DMS)
- AWS DataSync
- AWS Mainframe Modernization
- AWS Migration Hub
- AWS Transfer Family

### Networking and Content Delivery

- AWS App Mesh
- AWS Cloud Map
- AWS Direct Connect
- AWS Global Accelerator
- AWS Private 5G
- Amazon Route 53
- Amazon Route 53 Application Recovery Controller
- Amazon VPC IP Address Manager (IPAM)

### Security, Identity, and Compliance

- AWS Certificate Manager (ACM)
- AWS CloudHSM
- Amazon Cognito
- Amazon Detective
- AWS Directory Service
- AWS Firewall Manager
- Amazon GuardDuty
- AWS IAM Identity Center
- AWS Payment Cryptography
- AWS Private Certificate Authority
- AWS Resource Access Manager (AWS RAM)
- AWS Security Hub
- Amazon Security Lake
- AWS Shield
- AWS Signer
- Amazon Verified Permissions
- AWS WAF

### Storage

- AWS Backup
- AWS Elastic Disaster Recovery

## Cambios respecto a la versión 1.0

- **Añadidos a in scope:** Amazon Aurora, Amazon Bedrock AgentCore, Kiro, Strands Agents, Amazon Q, Amazon SageMaker JumpStart, AWS Transform.

> ⚠️ PENDIENTE DE VERIFICAR: la página de revisiones indica que Amazon Q se añadió a la lista in scope, pero la lista actual de servicios no lo incluye (sí incluye Amazon Quick). No tratar Amazon Q como servicio evaluable hasta aclararlo.

- **Eliminado de in scope:** Amazon MemoryDB.
- **Eliminados de out of scope:** AWS DeepComposer, Amazon FinSpace, Amazon Honeycode, AWS IAM Identity Center, AWS Marketplace, AWS Organizations, Amazon WorkDocs.

> ⚠️ PENDIENTE DE VERIFICAR: la página de revisiones dice que AWS DeepComposer, AWS IAM Identity Center, AWS Marketplace y AWS Organizations se eliminaron de la lista out of scope, pero la lista vigente los sigue incluyendo (comprobado el 2026-10-14). La lista de esta página se transcribe tal cual; en el curso se tratan como fuera de alcance.

Fuente: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/aif-01-revisions.html>
