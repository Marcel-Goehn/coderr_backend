
# API Reference

## Authentication

#### Creates a new user

```http
POST /api/registration/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `` | `` |  |

#### Request Body:

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

#### Success Response: 201 Created

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

#### User Login

```http
POST /api/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `` |  |

#### Request Body:

```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

#### Success Response: 200 OK

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

## Profile

#### Get detailed information about a user profile

```http
GET /api/profile/{pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |
| pk    | number | **Required**: ID of the profile |

#### Success Response: 200 OK

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "123456789",
  "description": "Business description",
  "working_hours": "9-17",
  "type": "business",
  "email": "max@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

#### Updates a user profile. You have to be the owner of the profile to be able to update it

```http
PATCH /api/profile/{pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |
| pk    | number | **Required**: ID of the profile |

#### Request Body:

```json
{
  "first_name": "Max",
  "last_name": "Mustermann",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "email": "new_email@business.de"
}
```

#### Success Response: 200 OK

```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "987654321",
  "description": "Updated business description",
  "working_hours": "10-18",
  "type": "business",
  "email": "new_email@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

#### Get a list of all business users profile

```http
GET /api/profiles/business/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
[
  {
    "user": 1,
    "username": "max_business",
    "first_name": "Max",
    "last_name": "Mustermann",
    "file": "profile_picture.jpg",
    "location": "Berlin",
    "tel": "123456789",
    "description": "Business description",
    "working_hours": "9-17",
    "type": "business"
  }
]
```

#### Get a list of all customer users profiles

```http
GET /api/profiles/customer/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
[
  {
    "user": 2,
    "username": "customer_jane",
    "first_name": "Jane",
    "last_name": "Doe",
    "file": "profile_picture_customer.jpg",
    "type": "customer"
  }
]
```

## Offer

#### Returns a list of all available offers.

```http
GET /api/offers/
```

| Query Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| creator_id    | integer | Filter the offers, to the creator of them |
| min_price    | float | Filter the offers to a minimum price |
| max_delivery_time    | integer | Filter the offers that have a delivery time less than the parameter |
| ordering    | string | Sorts the offers after the following fields: updated_at, min_price |
| search    | string | Searches in the fields "title" and "description" after matching characters |
| page_size    | integer | Returns a maximum of Items per page. Should be in sync with the frontend |

#### Success Response: 200 OK

```json
{
  "count": 1,
  "next": "http://127.0.0.1:8000/api/offers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "title": "Website Design",
      "image": null,
      "description": "Professionelles Website-Design...",
      "created_at": "2024-09-25T10:00:00Z",
      "updated_at": "2024-09-28T12:00:00Z",
      "details": [
        {
          "id": 1,
          "url": "/offerdetails/1/"
        },
        {
          "id": 2,
          "url": "/offerdetails/2/"
        },
        {
          "id": 3,
          "url": "/offerdetails/3/"
        }
      ],
      "min_price": 100,
      "min_delivery_time": 7,
      "user_details": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jdoe"
      }
    }
  ]
}
```

#### Creates a new offer. Every offer has to have 3 offer details. Only business user can create offers

```http
POST /api/offers/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Visitenkarte"
      ],
      "offer_type": "basic"
    },
    {
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

#### Response Success: 201 CREATED

```json
{
  "id": 1,
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "id": 1,
      "title": "Basic Design",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": 100,
      "features": [
        "Logo Design",
        "Visitenkarte"
      ],
      "offer_type": "basic"
    },
    {
      "id": 2,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": 200,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "id": 3,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 500,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

#### Returns a specific offer with the corresponding details.

```http
GET /api/offers/{id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
{
  "id": 66,
  "user": 114,
  "title": "Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "created_at": "2025-01-23T07:44:15.365773Z",
  "updated_at": "2025-01-23T07:44:15.365773Z",
  "details": [
    {
      "id": 199,
      "url": "http://127.0.0.1:8000/api/offerdetails/199/"
    },
    {
      "id": 200,
      "url": "http://127.0.0.1:8000/api/offerdetails/200/"
    },
    {
      "id": 201,
      "url": "http://127.0.0.1:8000/api/offerdetails/201/"
    }
  ],
  "min_price": 50,
  "min_delivery_time": 5
}

```

#### Updates a specific offer with it's details. Only the creator of the offer can update it

```http
PATCH /api/offers/{id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "title": "Updated Grafikdesign-Paket",
  "details": [
    {
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    }
  ]
}
```

#### Success Response: 200 OK

```json
{
  "id": 66,
  "title": "Updated Grafikdesign-Paket",
  "image": null,
  "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
  "details": [
    {
      "id": 199,
      "title": "Basic Design Updated",
      "revisions": 3,
      "delivery_time_in_days": 6,
      "price": 120,
      "features": [
        "Logo Design",
        "Flyer"
      ],
      "offer_type": "basic"
    },
    {
      "id": 200,
      "title": "Standard Design",
      "revisions": 5,
      "delivery_time_in_days": 10,
      "price": 120,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier"
      ],
      "offer_type": "standard"
    },
    {
      "id": 201,
      "title": "Premium Design",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": 150,
      "features": [
        "Logo Design",
        "Visitenkarte",
        "Briefpapier",
        "Flyer"
      ],
      "offer_type": "premium"
    }
  ]
}
```

#### Deletes a specific offer. Only the creator of the offer can delete it

```http
DELETE /api/offers/{id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 204 NO CONTENT

#### Returns a detail of a specific offer

```http
GET /api/offerdetails/{id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
{
  "id": 1,
  "title": "Basic Design",
  "revisions": 2,
  "delivery_time_in_days": 5,
  "price": 100,
  "features": [
    "Logo Design",
    "Visitenkarte"
  ],
  "offer_type": "basic"
}
```

## Order

#### Returns a list of orders that are associated with the authenticated user

```http
GET /api/orders/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "customer_user": 1,
    "business_user": 2,
    "title": "Logo Design",
    "revisions": 3,
    "delivery_time_in_days": 5,
    "price": 150,
    "features": [
      "Logo Design",
      "Visitenkarten"
    ],
    "offer_type": "basic",
    "status": "in_progress",
    "created_at": "2024-09-29T10:00:00Z",
    "updated_at": "2024-09-30T12:00:00Z"
  }
]
```

#### Creates a new order based on an offer detail. Only users of type customer are allowed to create orders

```http
POST /api/orders/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "offer_detail_id": 1
}
```

#### Success Response: 201 CREATED

```json
{
  "id": 1,
  "customer_user": 1,
  "business_user": 2,
  "title": "Logo Design",
  "revisions": 3,
  "delivery_time_in_days": 5,
  "price": 150,
  "features": [
    "Logo Design",
    "Visitenkarten"
  ],
  "offer_type": "basic",
  "status": "in_progress",
  "created_at": "2024-09-29T10:00:00Z"
}
```

#### Updates the status of a specific order. Possible values are: in_progress, completed and cancelled. Only user of type business can update a order

```http
PATCH /api/orders/{id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "status": "completed"
}
```

#### Success Response: 200 OK

```json
{
  "id": 1,
  "customer_user": 1,
  "business_user": 2,
  "title": "Logo Design",
  "revisions": 3,
  "delivery_time_in_days": 5,
  "price": 150,
  "features": [
    "Logo Design",
    "Visitenkarten"
  ],
  "offer_type": "basic",
  "status": "completed",
  "created_at": "2024-09-29T10:00:00Z",
  "updated_at": "2024-09-30T15:00:00Z"
}
```

#### Deletes a specific order. Only admin users (is_staff) can do this action

```http
DELETE /api/orders/{id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 204 No Content

#### Returns a list of all orders that are in_progress for a specific business user

```http
GET /api/order-count/{business_user_id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
{
  "order_count": 5
}
```

#### Returns a list of all orders that are completed for a specific business user

```http
GET /api/completed-order-count/{business_user_id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 200 OK

```json
{
  "completed_order_count": 10
}
```

## Review

#### Returns a list of all reviews

```http
GET /api/reviews/
```

| Query Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |
| business_user_id    | integer | ID of a business user for filtering corresponding reviews |
| reviewer_id    | integer | ID of a user that created reviews |
| ordering    | string | It can get sorted for the following fields: updated_at, rating |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "business_user": 2,
    "reviewer": 3,
    "rating": 4,
    "description": "Sehr professioneller Service.",
    "created_at": "2023-10-30T10:00:00Z",
    "updated_at": "2023-10-31T10:00:00Z"
  },
  {
    "id": 2,
    "business_user": 5,
    "reviewer": 3,
    "rating": 5,
    "description": "Top Qualität und schnelle Lieferung!",
    "created_at": "2023-09-20T10:00:00Z",
    "updated_at": "2023-09-20T12:00:00Z"
  }
]
```

#### Creats a new review. Only users of type customer can give reviews to business users. A customer can only give one review per business user

```http
POST /api/reviews/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "business_user": 2,
  "rating": 4,
  "description": "Alles war toll!"
}
```

#### Success Response: 201 CREATED

```json
{
  "id": 3,
  "business_user": 2,
  "reviewer": 3,
  "rating": 4,
  "description": "Alles war toll!",
  "created_at": "2023-10-30T15:30:00Z",
  "updated_at": "2023-10-30T15:30:00Z"
}
```

#### Updates a specific review. Only the creator of the review can update it. Only "rating" and "description" are editable

```http
PATCH /api/reviews/{id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Request Body:

```json
{
  "rating": 5,
  "description": "Noch besser als erwartet!"
}
```

#### Success Response: 200 OK

```json
{
  "id": 1,
  "business_user": 2,
  "reviewer": 3,
  "rating": 5,
  "description": "Noch besser als erwartet!",
  "created_at": "2023-10-30T10:00:00Z",
  "updated_at": "2023-11-01T08:00:00Z"
}
```

##### Deletes a specific review. Only the creator of the review can delete it

```http
DELETE /api/reviews/{id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: `Token <token>` |

#### Success Response: 204 NO CONTENT

## Base Information

#### Returns general informations about the platform. It includes: Review count, average rating, count of all business profiles and count of all available offers

#### Success Response: 200 OK

```json
{
  "review_count": 10,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 150
}
```