---
title: Questionnaire
slug: questionnaire
summary: Binary screening responses with a separate bilingual item schema.
flag: questionnaire_available
status: partial
---

## Task protocol

Responses are stored in `questionnaire_responses.csv`; item wording and encoding are stored in `questionnaire_schema.csv`.

<div class="todo">TODO — pending clinical team: confirm administration instructions, whether assistance was permitted, question order, app version and the clinically reviewed domain assigned to each item.</div>

## Sensor and format

This is a table-backed modality rather than a sensor recording. Each response column is binary: `0 = No` and `1 = Yes`. Thai and English wording, response type and encoding are supplied in the schema table.

## Preprocessing

Questionnaire responses are represented as individual CSV columns rather than a comma-separated string inside JSON. Direct and backend identifiers are removed; only the release subject pattern remains.

## Quality control

Validation checks that response values follow the declared encoding, that schema IDs match response columns, and that participant membership agrees with `metadata.csv`. Clinical domain assignment remains pending.

## Example structure

```text
questionnaire_responses.csv
subject_id,q01,q02,...
S####,0,1,...

questionnaire_schema.csv
question_id,question_text_th,question_text_en,response_type,encoding
```

Source: `CheckPD_Local_Agent_Context.md` §7.
