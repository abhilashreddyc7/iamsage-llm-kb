This covers a foundational security concept.

```markdown data/raw/principle_of_least_privilege.md
# Source: General IAM Best Practices

# Topic: The Principle of Least Privilege (PoLP)

## Definition

The Principle of Least Privilege is a foundational concept in information security. It dictates that a user, program, or process should only be given the minimum levels of access – or permissions – needed to perform its specific job or function.

## Why is it Important?

- **Reduces Attack Surface:** If an account is compromised, the attacker only gains access to the limited permissions of that account, preventing them from moving laterally through the system with elevated rights.
- **Minimizes Scope of Errors:** Accidental misuse of permissions is less damaging. A user with limited rights cannot accidentally delete critical data or reconfigure a system they don't need access to.
- **Improves Auditability and Compliance:** It is easier to audit and manage user permissions when they are tightly controlled and based on job roles. This is a key requirement for compliance standards like GDPR, HIPAA, and SOX.

## Implementation

1. **Default Deny:** Start with a "deny-all" policy and only grant permissions as needed.
2. **Role-Based Access Control (RBAC):** Group users into roles based on their job responsibilities and assign permissions to the roles, not directly to individual users.
3. **Just-in-Time (JIT) Access:** Grant temporary, elevated permissions only for the duration that they are needed, rather than granting standing access.
4. **Regular Access Reviews:** Periodically review and certify user access to ensure that permissions are still required and appropriate for their roles. Unused or excessive permissions should be revoked.
```
