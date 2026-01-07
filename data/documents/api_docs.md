# Internal API Documentation Standards

## Purpose
This document defines the required structure and standards for all **internal API documentation**.

## Required Documentation Location

- All APIs **must** have documentation published in the **central API portal**  
  (Swagger/OpenAPI format is **preferred**)
- Source documentation files are stored in the repository at:  
  `/docs/api/` (alongside the related code)

## Mandatory Sections

Every API documentation **must** include the following sections:

1. **API Overview & Purpose**  
   High-level description of what the API does and its intended use cases

2. **Base URL & Authentication method**  
   - Base URL structure  
   - Supported authentication mechanisms

3. **Rate limits & Quotas**  
   Global and per-endpoint limits

4. **Error codes & handling**  
   Standard error format and common error codes

5. **Authentication & Authorization**  
   - JWT, API keys, OAuth scopes, etc.  
   - Required headers and token formats

6. **Endpoints** — detailed list containing for each endpoint:
   - HTTP method
   - Path
   - Description/purpose
   - Required permissions/roles
   - Request parameters:
     - Path parameters
     - Query parameters
     - Request body (schema)
   - Response structure:
     - Success response (schema)
     - Error responses (schemas)
   - **Example request/response** (valid JSON)

## Versioning Requirements

- All APIs **must** be versioned (e.g., `/v1/`, `/v2/`)
- **Breaking changes** require a new **major** version
- **Deprecation notice**  
  Minimum **90 days** advance notice for deprecated endpoints/versions

## Documentation Standards

- Use **OpenAPI 3.0+** specification
- Include complete definitions for:
  - All **enums**
  - All **schemas** (request/response)
  - Realistic **examples**
- Document **rate limits** per endpoint and/or per user/role
- Documentation **must** be updated **before** production deployment
- Documentation is part of the **code review** process

## Ownership & Maintenance

- **API owner** (owning team / technical lead) is responsible for keeping documentation current
- All changes to documentation **must** follow the same review process as code changes

## Incident Classification

**Out-of-date**, **incomplete**, or **missing** API documentation is classified as a **Severity 3** incident.