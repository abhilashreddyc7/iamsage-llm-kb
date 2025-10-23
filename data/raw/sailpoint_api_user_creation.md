This provides a practical code-based example, useful for developers.

````markdown data/raw/sailpoint_api_user_creation.md
# Source: SailPoint Developer Community

# Topic: Creating a SailPoint Identity via API

## Overview

You can programmatically create identities in SailPoint IdentityNow using the v3 APIs. This is useful for custom scripts or integrating with systems that do not have a standard connector.

### Endpoint

The primary endpoint for creating accounts is:
`POST /v3/accounts`

### Request Body

The request body must contain the source ID and the attributes for the new account. A unique identifier, like `uid` or `employeeId`, is essential.

```json
{
  "sourceId": "2c9180857893f12901789445213d2122",
  "attributes": {
    "uid": "john.doe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "department": "Engineering"
  }
}
```
````

### Authentication

Authentication is handled via OAuth 2.0. You must first obtain a Bearer Token by making a request to the `/oauth/token` endpoint with your Client ID and Client Secret. This token is then included in the `Authorization` header of your API request.

### Important Considerations

- **Source:** You must provide the `sourceId` of an authoritative source configured in IdentityNow.
- **Correlation:** After the account is created, an identity will be created and correlated based on the identity profile's correlation logic. If an identity with a matching attribute (e.g., email) already exists, the new account will be linked to it. Otherwise, a new identity is created.
- **Lifecycle State:** The identity will be created in the "active" lifecycle state by default, unless specified otherwise by source configurations.

```

```
