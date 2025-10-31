# Steam Analytics Platform API Documentation

## Overview
The Steam Analytics Platform provides RESTful APIs for accessing gaming analytics data, AI insights, and platform management.

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>