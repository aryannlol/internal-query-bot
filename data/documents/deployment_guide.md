# Software Deployment Guide

## Purpose
This document outlines the standard process for deploying software changes to production environments.

## Environments
**Development → Staging → Production**

All changes **must** progress through this sequence unless explicitly approved otherwise by Engineering Director.

## Deployment Types
- Routine releases (planned features, improvements, bug fixes)
- Hotfixes (critical production issues requiring immediate action)
- Configuration changes
- Infrastructure updates

## Required Approvals

| Stage                              | Approver(s)                                      | Notes                                      |
|------------------------------------|--------------------------------------------------|--------------------------------------------|
| Code / Artifact                    | Peer code review + Tech Lead                     | Mandatory for all changes                  |
| Deployment to Staging              | Development Team Lead                            | —                                          |
| Deployment to Production           | Product Manager + Engineering Manager            | Required during business hours             |
| Changes after 17:00 or on weekends | Engineering Director + On-call Engineer          | Emergency exception process applies        |

## Standard Deployment Process

1. Create release branch from `main`
2. Implement changes and pass all automated tests (CI pipeline)
3. Submit Pull Request → complete **peer code review**
4. Merge to `main` after approval
5. Deploy to **Staging** environment
6. **QA + Product team verification** in Staging
7. Schedule production deployment window  
   - Minimum **48 hours** advance notice (unless emergency/hotfix)
8. Perform deployment during the approved change window
9. Actively **monitor** for at least **30 minutes** post-deployment
10. Document and (where applicable) **pre-test rollback plan**

## Emergency / Hotfix Deployment Process

1. Document the issue:
   - Severity
   - Customer/business impact
   - Root cause (if known)
2. Obtain **verbal approval** from:
   - Engineering Manager  
   - Product Manager
3. Proceed with deployment (usually to production directly)
4. Actively monitor during and after deployment
5. Complete formal **post-incident review** within **72 hours**

## Rollback Criteria
Immediate rollback is required if **any** of the following is observed:

- Error rate increases by **≥ 5%** (compared to pre-deployment baseline)
- Critical functionality failure
- Performance degradation **> 30%** (key metrics: latency, throughput)
- Widespread customer-reported major issues

## Logging Requirement
**All deployments** (standard, hotfix, config, infra) **must** be recorded in the central **deployment tracking system**.

---

**Last Updated:** December 25, 2025  
**Process Owner:** Engineering Leadership Team