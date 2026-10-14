# Dominio 3: Applications of Foundation Models

- **Fuente:** <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain3.html>
- **Fecha de consulta:** 2026-10-14
- **Versión de la guía:** 1.1 (publicada el 30 de abril de 2026)
- **Peso en el examen:** 28 % del contenido puntuable

Texto literal en inglés de la guía oficial. Cada objetivo se numera como `N.M.K` (el orden de aparición, convención de la página de revisiones de AWS). No traducir ni parafrasear aquí.

## Task Statement 3.1

Describe design considerations for applications that use foundation models (FMs).

### Objectives

1. **3.1.1** Identify selection criteria to choose FMs (for example, cost, modality, latency, multi-lingual, model size, model complexity, customization, input/output length, prompt caching).
2. **3.1.2** Describe the effect of inference parameters on model responses (for example, temperature, input/output length).
3. **3.1.3** Define Retrieval Augmented Generation (RAG) and describe its business applications (for example, Amazon Bedrock Knowledge Bases).
4. **3.1.4** Identify AWS services that help store embeddings within vector databases (for example, Amazon OpenSearch Service, Amazon Aurora, Amazon Neptune, Amazon RDS for PostgreSQL).
5. **3.1.5** Explain the cost tradeoffs of various approaches to FM customization (for example, pre-training, fine-tuning, in-context learning, RAG, model distillation).
6. **3.1.6** Define the role of AI agents and describe AI agents' business applications.

## Task Statement 3.2

Choose effective prompt engineering techniques.

### Objectives

1. **3.2.1** Define the concepts and constructs of prompt engineering (for example, context, instruction, negative prompts).
2. **3.2.2** Define techniques for prompt engineering (for example, chain-of-thought, zero-shot, single-shot, few-shot, prompt templates).
3. **3.2.3** Identify and describe the benefits and best practices for prompt engineering (for example, response quality improvement, experimentation, guardrails, discovery, specificity and concision, using multiple comments).
4. **3.2.4** Define potential risks and limitations of prompt engineering (for example, exposure, poisoning, hijacking, jailbreaking).
5. **3.2.5** Describe prompt versioning and management strategies that use Amazon Bedrock Prompt Management.

## Task Statement 3.3

Describe the training and fine-tuning process for FMs.

### Objectives

1. **3.3.1** Describe the key elements of training an FM (for example, pre-training, fine-tuning, continuous pre-training, distillation).
2. **3.3.2** Define methods for fine-tuning an FM (for example, instruction tuning, adapting models for specific domains, transfer learning, continuous pre-training).
3. **3.3.3** Describe how to prepare data to fine-tune an FM (for example, data curation, governance, size, labeling, representativeness, reinforcement learning from human feedback [RLHF]).

## Task Statement 3.4

Describe methods to evaluate FM performance.

### Objectives

1. **3.4.1** Determine approaches to evaluate FM performance (for example, human-in-the-loop evaluation, benchmark datasets, Amazon Bedrock Model Evaluation).
2. **3.4.2** Identify relevant metrics to assess FM performance (for example, Recall-Oriented Understudy for Gisting Evaluation [ROUGE], Bilingual Evaluation Understudy [BLEU], BERTScore, LLM-as-a-judge).
3. **3.4.3** Determine whether an FM effectively meets business objectives (for example, productivity, user engagement, task engineering).
4. **3.4.4** Identify approaches to evaluate the performance of applications built with FM (for example, RAG, agents, workflows).
5. **3.4.5** Identify business objective alignment metrics for AI applications (for example, task completion rate, user satisfaction, cost per interaction).
