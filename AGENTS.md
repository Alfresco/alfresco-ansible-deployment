# AGENTS.md

## Project Overview

Ansible playbooks for deploying Alfresco Content Services (ACS) on VM/bare-metal.
Main entrypoint: `playbooks/acs.yml`. Roles in `roles/` (17 components: activemq, elasticsearch, nginx, postgres, repository, tomcat, etc.).

## Setup

```bash
pipenv install --dev --python $(cat .python-version)
pipenv shell  # or prefix commands with `pipenv run`
```

Required: Python 3.11, Docker (for role tests), direnv recommended.

## Key Commands

```bash
# Lint (runs ansible-lint + yamllint + djlint + pymarkdown + detect-secrets)
pipenv run pre-commit run --all-files

# Ansible-lint only
pipenv run ansible-lint

# Role unit test (Docker-based, run from role directory)
cd roles/<role_name>
molecule converge    # provision
molecule verify      # run tests
molecule destroy     # cleanup
MOLECULE_ROLE_IMAGE=ubuntu:24.04 molecule converge  # different OS

# Integration tests (requires AWS creds + Nexus creds, see .envrc)
molecule -e molecule/default/vars-rhel8.yml test

# Docker-only full integration (no AWS needed)
molecule test -s local
```

## Repository Structure

- `playbooks/` - Main playbooks (acs.yml, pki.yml, platform-restart.yml, etc.)
- `roles/` - 17 Ansible roles, each with own `molecule/` tests
- `vars/acs*.yml` - Version-specific variables per ACS release (acs23, acs25, acs26, acs74)
- `molecule/` - Root-level integration test scenarios (default=EC2, docker_community, docker_enterprise, multimachine, etc.)
- `group_vars/` - Inventory group variables
- `docs/` - GitHub Pages documentation (Jekyll)
- `scripts/` - Utility scripts (version table generation, AWS cleanup)

## CI Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `precommit.yml` | All PRs + push to master | pre-commit hooks (lint, secrets, formatting) |
| `community.yml` | PRs/push to master (non-docs) | Role molecule tests on Docker (community edition) |
| `enteprise.yml` | PRs with `ec2-test` label + push to master | EC2 integration tests (needs Nexus secrets) |
| `bumpVersions.yml` | Manual dispatch | Updatecli version bumps |
| `release.yml` | Tag push (`v*`) | Build release artifacts |
| `docs.yml` | Docs changes | Publish GitHub Pages |

## Conventions

- **Linting**: ansible-lint with `name[template]` and `galaxy` rules skipped; `molecule/` excluded
- **YAML style**: yamllint with relaxed rules (no line-length limit, indentation disabled, truthy disabled)
- **Jinja templates**: linted by djLint (config in `.djlintrc`)
- **Markdown**: pymarkdown for README and docs/ only
- **Secrets**: detect-secrets with baseline file `.secrets.baseline`
- **Pre-commit**: runs `generate-comp-ver-table.py` on every commit (auto-generates version table)
- **New distro support**: add to `supported_os` in `vars/acsXX.yml`, prefer `vars` files over conditional tasks

## Environment Variables (Integration Tests)

Defined in `.envrc`, secrets in `.env.credentials` (gitignored):
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- `NEXUS_USERNAME`, `NEXUS_PASSWORD` (enterprise artifact downloads)
- `CLONE_GITHUB_TOKEN`
- `ANSIBLE_VAULT_PASSWORD_FILE` → `.vault_pass.txt`

## Gotchas

- Enterprise workflow file is misspelled: `enteprise.yml` (not a typo to fix - it's the actual filename)
- The `ec2-test` label on a PR triggers enterprise integration tests
- `next/**` branches have special CI behavior (skip community docker tests)
- Vault password file `.vault_pass.txt` must exist locally for encrypted vars
- Galaxy dependencies installed from `requirements.yml`
