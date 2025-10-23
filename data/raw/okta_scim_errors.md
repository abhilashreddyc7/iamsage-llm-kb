# Source: Okta Documentation

# Topic: Common SCIM Provisioning Errors with Okta

## Overview

System for Cross-domain Identity Management (SCIM) is an open standard that allows for the automation of user provisioning. When integrating an application with Okta via SCIM, several common errors can occur.

### Error: 401 Unauthorized

This is the most common error and typically points to an issue with the Bearer Token.
**Cause:** The API token configured in the Okta app integration is invalid, expired, or does not have the necessary permissions in the target application.
**Solution:**

1. Verify the Bearer Token is an exact match with the one generated in your SCIM application.
2. Ensure the service account or user associated with the token has the required administrative privileges to create, update, and deactivate users.
3. Check if the token has expired.

### Error: 400 Bad Request

This error indicates a problem with the data being sent in the SCIM request payload.
**Cause:**

- A required attribute is missing (e.g., `userName` or `externalId`).
- An attribute value does not match the expected format (e.g., sending "N/A" for an email attribute that requires a valid email format).
- Mismatched attribute names in the Okta attribute mapping. For example, Okta is sending `user_name` but the SCIM server expects `userName`.
  **Solution:**

1. Review the SCIM server's API documentation for required attributes and expected data formats.
2. Use the "Preview Mapping" feature in Okta to check the data being sent for a sample user.
3. Ensure custom attribute mappings in Okta align perfectly with the SCIM app's schema.

### Error: 409 Conflict

This error means the SCIM server cannot process the request because it conflicts with an existing resource.
**Cause:** Attempting to create a user with a `userName` or `email` that already exists in the target application.
**Solution:**

1. Ensure the user does not already have an account in the downstream application.
2. Check your correlation logic. If you are not matching on the correct attributes, Okta may be trying to create a new user instead of linking to an existing one.
