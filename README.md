# sello
A simplified version of a platform to buy or sell items

Server IP: http://35.231.199.53/

## Contents
- Products
    - [Get all products](#Get-all-products)
    - [Create a product](#Create-a-product)
    - [Get a specific product](#Get-a-specific-product)
    - [Delete a product](#Delete-a-product)
    - [Buy a specific product](#Buy-a-specific-product)
- User
    - [Register an account](#Register-an-account)
    - [Login](#Login)
    - [Get information of current user](#Get-information-of-current-user)
    - [Update session](#Update-session)
- Categories
    - [Get all categories](#Get-all-categories)
    - [Get a specific category](#Get-a-specific-category)

### Get all products
`GET`  `/products/`
```json
Response 

{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Switch",
            "description": "video game console",
            "condition": "new",
            "price": 100.0,
            "sold": false,
            "seller_id": 1,
            "buyer_id": null,
            "categories": [
                {
                    "category": "video games"
                }
                "..."
            ]
        }
        "..."
    ]
}

```

### Create a product
`POST` `/products/`
```json
Request

{
    "name": "<USER INPUT>",
    "description": "<USER INPUT>",
    "condition": "<USER INPUT>",
    "price": "<USER INPUT>",
    "categories": "<USER INPUT, COMMA-SEPARATED CATEGORIES>"
}
```
```json
Response 

{
    "success": true,
    "data": {
        "id": 1,
        "name": "<USER INPUT FOR NAME>",
        "description": "<USER INPUT FOR DESCRIPTION>",
        "condition": "<USER INPUT FOR CONDITION>",
        "price": "<USER INPUT FOR PRICE>",
        "sold": false,
        "seller_id": 2,
        "buyer_id": null,
        "categories": [
            {
                "category": "<USER INPUT CATEGORY 1>"
            }
            "..."
        ]
    }
} 

```

### Get a specific product 
`GET` `/products/{id}/`
```json
Response 

{
    "success": true,
    "data":{
        "id": 1,
        "name": "Switch",
        "description": "video game console",
        "condition": "new",
        "price": 100.0,
        "sold": false,
        "seller_id": 1,
        "buyer_id": 2,
        "categories": [
            {
                "category": "video games"
            }
            "..."
        ]
    }
} 

```

### Delete a product
`DELETE` `/products/{id}/`
```json
Response

{
    "success": true,
    "data":{
        "id": 1,
        "name": "Switch",
        "description": "video game console",
        "condition": "new",
        "price": 100.0,
        "sold": false,
        "seller_id": 1,
        "buyer_id": null,
        "categories": [
            {
                "category": "video games"
            }
            "..."
        ]
    }
}

```

### Buy a specific product 
`POST` `/products/{id}/buy/`
```json
Response

{
    "success": true,
    "data":{
        "id": 1,
        "name": "Switch",
        "description": "video game console",
        "condition": "new",
        "price": 100.0,
        "sold": true,
        "seller_id": 1,
        "buyer_id": 2,
        "categories": [
            {
                "category": "video games"
            }
            "..."
        ]
    }
}

```

### Register an account
`POST` `/register/`
```json
Request

{
    "username": "<USER INPUT>",
    "email": "<USER INPUT>",
    "password": "<USER INPUT>"
}
```
```json
Response

{
    "success": true,
    "data": {
        "session_token": "<TOKEN>",
        "session_expiration": "<SESSION EXPIRATION DATE>",
        "update_token": "<TOKEN>"
    }
}
```

### Login
`POST` `/login/`
```json
Request

{
    "email": "<USER INPUT>",
    "password": "<USER INPUT>"
}
```
```json
Response

{
    "success": true,
    "data": {
        "session_token": "<TOKEN>",
        "session_expiration": "<SESSION EXPIRATION DATE>",
        "update_token": "<TOKEN>"
    }
}
```

### Get information of current user
`GET` `/user/`
```json
Response

{
    "success": true,
    "data": {
        "id": 1,
        "username": "<USER USERNAME>",
        "email": "<USER INPUT FOR EMAIL>",
        "selling": [
            {
                "id": 1,
                "name": "Switch",
                "description": "video game console",
                "condition": "new",
                "price": 100.0,
                "sold": false,
                "seller_id": 1,
                "buyer_id": null
            }
            "..."
        ],
        "buying": []
    }
}
```

### Update session
`POST` `/session/`
```
Request

new session token
```
```json
Response

{
    "success": true,
    "data": {
        "session_token": "<TOKEN>",
        "session_expiration": "<SESSION EXPIRATION DATE>",
        "update_token": "<TOKEN>"
    }
}
```

### Get all categories
`GET` `/categories/`
```json
{
    "success": true,
    "data": [
        {
            "category": "games",
            "products": [
                {
                    "id": 1,
                    "name": "Switch",
                    "description": "video game console",
                    "condition": "new",
                    "price": 100.0,
                    "sold": false,
                    "seller_id": 1,
                    "buyer_id": null
                }
            "..."
            ]
        },
        "..."
    ]
}
```

### Get a specific category
`GET` `/categories/{id}/`
```json
{
    "success": true,
    "data": {
        "category": "games",
        "products": [
            {
                "id": 1,
                "name": "Switch",
                "description": "video game console",
                "condition": "new",
                "price": 100.0,
                "sold": false,
                "seller_id": 1,
                "buyer_id": null
            }
        "..."
        ]
    }
}
```













