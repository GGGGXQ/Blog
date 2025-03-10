# Post  API 接口文档
## 概述

`post` 子应用提供了与帖子相关的功能，包括帖子的创建、查看、删除、点赞、评论以及趋势话题的获取。本文档详细描述了每个接口的请求方法、URL、参数及返回数据。

## 身份验证

所有接口均需要用户登录并提供身份验证。身份验证通过 JWT 令牌实现，用户需在请求头中提供令牌，格式如下：

```
Authorization: Bearer <token>
```

未提供有效令牌的请求将被拒绝。

---

## 接口列表

### 1. 获取帖子列表

#### 接口名称
获取帖子列表

#### 接口描述
获取当前用户及其好友的帖子列表，支持根据趋势话题过滤。

#### 请求方法
`GET`

#### 请求 URL
`/`

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述           |
|--------|--------|----------|----------------|
| trend  | string | 否       | 趋势话题标签   |

#### 返回参数

| 参数名               | 类型   | 描述                 |
|----------------------|--------|----------------------|
|                      | array  | 帖子列表             |

**返回参数（数组中每个对象）：**

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 帖子 ID（UUID 格式）  |
| body                  | string | 帖子内容              |
| is_private            | boolean| 是否为私密帖子        |
| likes_count           | int    | 点赞数量              |
| comments_count        | int    | 评论数量              |
| is_liked              | boolean| 当前用户是否已点赞    |
| created_by            | object | 发帖人信息            |
| created_at_formatted  | string | 发帖时间的格式化字符串|
| attachments           | array  | 附件列表              |

#### 示例

**请求：**
```
GET /?trend=example
Authorization: Bearer <token>
```

**响应：**
```json
[
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "body": "This is a post with #example",
        "is_private": false,
        "likes_count": 10,
        "comments_count": 5,
        "is_liked": true,
        "created_by": {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "user1",
            "email": "user1@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/user1.jpg"
        },
        "created_at_formatted": "1天前",
        "attachments": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "get_image": "https://example.com/images/attachment.jpg"
            }
        ]
    }
]
```

---

### 2. 获取帖子详情

#### 接口名称
获取帖子详情

#### 接口描述
获取指定帖子的详细信息，包括评论和附件。

#### 请求方法
`GET`

#### 请求 URL
`/<uuid:pk>/`

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| pk     | uuid | 是       | 帖子 ID     |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| post                  | object | 帖子详情              |

**返回参数（post 对象）：**

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 帖子 ID（UUID 格式）  |
| body                  | string | 帖子内容              |
| likes_count           | int    | 点赞数量              |
| comments_count        | int    | 评论数量              |
| created_by            | object | 发帖人信息            |
| created_at_formatted  | string | 发帖时间的格式化字符串|
| comments              | array  | 评论列表              |
| attachments           | array  | 附件列表              |

#### 示例

**请求：**
```
GET /123e4567-e89b-12d3-a456-426614174000/
Authorization: Bearer <token>
```

**响应：**
```json
{
    "post": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "body": "This is a post",
        "likes_count": 10,
        "comments_count": 5,
        "created_by": {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "user1",
            "email": "user1@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/user1.jpg"
        },
        "created_at_formatted": "1天前",
        "comments": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "body": "Nice post!",
                "created_by": {
                    "id": "123e4567-e89b-12d3-a456-426614174003",
                    "name": "user2",
                    "email": "user2@example.com",
                    "friends_count": 5,
                    "posts_count": 15,
                    "get_avatar": "https://example.com/avatars/user2.jpg"
                },
                "created_at_formatted": "1小时前"
            }
        ],
        "attachments": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174004",
                "get_image": "https://example.com/images/attachment.jpg"
            }
        ]
    }
}
```

---

### 3. 获取用户帖子列表

#### 接口名称
获取用户帖子列表

#### 接口描述
获取指定用户的帖子列表，私密帖子仅对好友和自己可见。

#### 请求方法
`GET`

#### 请求 URL
`/profile/<uuid:id>/`

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| id     | uuid | 是       | 用户 ID     |

#### 返回参数

| 参数名                      | 类型    | 描述                  |
|-----------------------------|---------|-----------------------|
| posts                       | array   | 帖子列表              |
| user                        | object  | 用户信息              |
| can_send_friendship_request | boolean | 是否可以发送好友请求  |

**返回参数（posts 数组中每个对象）：**

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 帖子 ID（UUID 格式）  |
| body                  | string | 帖子内容              |
| is_private            | boolean| 是否为私密帖子        |
| likes_count           | int    | 点赞数量              |
| comments_count        | int    | 评论数量              |
| is_liked              | boolean| 当前用户是否已点赞    |
| created_by            | object | 发帖人信息            |
| created_at_formatted  | string | 发帖时间的格式化字符串|
| attachments           | array  | 附件列表              |

**返回参数（user 对象）：**

| 参数名        | 类型   | 描述                  |
|---------------|--------|-----------------------|
| id            | string | 用户 ID（UUID 格式）  |
| name          | string | 用户名                |
| email         | string | 用户邮箱              |
| friends_count | int    | 好友数量              |
| posts_count   | int    | 帖子数量              |
| get_avatar    | string | 用户头像 URL          |

#### 示例

**请求：**
```
GET /profile/123e4567-e89b-12d3-a456-426614174001/
Authorization: Bearer <token>
```

**响应：**
```json
{
    "posts": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "body": "This is a post",
            "is_private": false,
            "likes_count": 10,
            "comments_count": 5,
            "is_liked": true,
            "created_by": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "user1",
                "email": "user1@example.com",
                "friends_count": 10,
                "posts_count": 20,
                "get_avatar": "https://example.com/avatars/user1.jpg"
            },
            "created_at_formatted": "1天前",
            "attachments": []
        }
    ],
    "user": {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "user1",
        "email": "user1@example.com",
        "friends_count": 10,
        "posts_count": 20,
        "get_avatar": "https://example.com/avatars/user1.jpg"
    },
    "can_send_friendship_request": false
}
```

---

### 4. 创建帖子

#### 接口名称
创建帖子

#### 接口描述
创建新的帖子，支持上传附件。

#### 请求方法
`POST`

#### 请求 URL
`/create/`

#### 请求参数

| 参数名     | 类型   | 是否必填 | 描述           |
|------------|--------|----------|----------------|
| body       | string | 是       | 帖子内容       |
| is_private | boolean| 否       | 是否为私密帖子 |
| image      | file   | 否       | 附件图片       |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 帖子 ID（UUID 格式）  |
| body                  | string | 帖子内容              |
| is_private            | boolean| 是否为私密帖子        |
| likes_count           | int    | 点赞数量              |
| comments_count        | int    | 评论数量              |
| is_liked              | boolean| 当前用户是否已点赞    |
| created_by            | object | 发帖人信息            |
| created_at_formatted  | string | 发帖时间的格式化字符串|
| attachments           | array  | 附件列表              |

#### 示例

**请求：**
```
POST /create/
Authorization: Bearer <token>
Content-Type: multipart/form-data

body=This is a new post
is_private=false
image=<file>
```

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "body": "This is a new post",
    "is_private": false,
    "likes_count": 0,
    "comments_count": 0,
    "is_liked": false,
    "created_by": {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "user1",
        "email": "user1@example.com",
        "friends_count": 10,
        "posts_count": 21,
        "get_avatar": "https://example.com/avatars/user1.jpg"
    },
    "created_at_formatted": "刚刚",
    "attachments": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "get_image": "https://example.com/images/attachment.jpg"
        }
    ]
}
```

---

### 5. 删除帖子

#### 接口名称
删除帖子

#### 接口描述
删除指定帖子（仅限发帖人）。

#### 请求方法
`DELETE`

#### 请求 URL
`/<uuid:pk>/delete/`

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| pk     | uuid | 是       | 帖子 ID     |

#### 返回参数

| 参数名  | 类型   | 描述     |
|---------|--------|----------|
| message | string | 操作结果 |

#### 示例

**请求：**
```
DELETE /123e4567-e89b-12d3-a456-426614174000/delete/
Authorization: Bearer <token>
```

**响应：**
```json
{
    "message": "post deleted"
}
```

---

### 6. 举报帖子

#### 接口名称
举报帖子

#### 接口描述
举报指定帖子。

#### 请求方法
`POST`

#### 请求 URL
`/<uuid:pk>/report/`

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| pk     | uuid | 是       | 帖子 ID     |

#### 返回参数

| 参数名  | 类型   | 描述     |
|---------|--------|----------|
| message | string | 操作结果 |

#### 示例

**请求：**
```
POST /123e4567-e89b-12d3-a456-426614174000/report/
Authorization: Bearer <token>
```

**响应：**
```json
{
    "message": "post reported"
}
```

---

### 7. 点赞帖子

#### 接口名称
点赞帖子

#### 接口描述
对指定帖子进行点赞或取消点赞。

#### 请求方法
`POST`

#### 请求 URL
`/<uuid:pk>/like/`

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| pk     | uuid | 是       | 帖子 ID     |

#### 返回参数

| 参数名  | 类型   | 描述     |
|---------|--------|----------|
| message | string | 操作结果 |

#### 示例

**请求：**
```
POST /123e4567-e89b-12d3-a456-426614174000/like/
Authorization: Bearer <token>
```

**响应（点赞）：**
```json
{
    "message": "like created"
}
```

**响应（取消点赞）：**
```json
{
    "message": "dislike created"
}
```

---

### 8. 评论帖子

#### 接口名称
评论帖子

#### 接口描述
对指定帖子发表评论。

#### 请求方法
`POST`

#### 请求 URL
`/<uuid:pk>/comment/`

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述        |
|--------|--------|----------|-------------|
| pk     | uuid   | 是       | 帖子 ID     |
| body   | string | 是       | 评论内容    |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 评论 ID（UUID 格式）  |
| body                  | string | 评论内容              |
| created_by            | object | 评论人信息            |
| created_at_formatted  | string | 评论时间的格式化字符串|

#### 示例

**请求：**
```
POST /123e4567-e89b-12d3-a456-426614174000/comment/
Authorization: Bearer <token>
Content-Type: application/json

{
    "body": "Nice post!"
}
```

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174002",
    "body": "Nice post!",
    "created_by": {
        "id": "123e4567-e89b-12d3-a456-426614174003",
        "name": "user2",
        "email": "user2@example.com",
        "friends_count": 5,
        "posts_count": 15,
        "get_avatar": "https://example.com/avatars/user2.jpg"
    },
    "created_at_formatted": "1小时前"
}
```

---

### 9. 获取趋势话题

#### 接口名称
获取趋势话题

#### 接口描述
获取所有趋势话题。

#### 请求方法
`GET`

#### 请求 URL
`/trends/`

#### 请求参数
无

#### 返回参数

| 参数名               | 类型   | 描述                 |
|----------------------|--------|----------------------|
|                      | array  | 趋势话题列表         |

**返回参数（数组中每个对象）：**

| 参数名     | 类型   | 描述           |
|------------|--------|----------------|
| id         | string | 趋势 ID        |
| hashtag    | string | 话题标签       |
| occurences | int    | 出现次数       |

#### 示例

**请求：**
```
GET /trends/
Authorization: Bearer <token>
```

**响应：**
```json
[
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "hashtag": "#example",
        "occurences": 100
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "hashtag": "#trend",
        "occurences": 50
    }
]
```

---

## 注意事项

1. **数据格式**  
   所有接口返回的数据均为 JSON 格式。

2. **身份验证**  
   所有接口均需要用户登录并提供有效的 JWT 令牌。

3. **帖子可见性**  
   - 私密帖子仅对发帖人及其好友可见。
   - 在获取用户帖子列表时，会根据当前用户的身份过滤私密帖子。

4. **附件上传**  
   - 创建帖子时支持上传图片附件，需使用 `multipart/form-data` 格式。
   - 附件图片的 URL 通过 `get_image` 方法获取。

5. **点赞逻辑**  
   - 用户可以对帖子点赞或取消点赞。
   - 点赞操作会创建通知（`post_like` 类型）。

6. **评论逻辑**  
   - 用户可以对帖子发表评论。
   - 评论操作会创建通知（`post_comment` 类型）。

7. **趋势话题**  
   - 趋势话题的获取不依赖于用户身份，但仍需身份验证。

8. **错误处理**  
   - 当前代码未显式处理异常情况（如帖子不存在或用户无权限访问指定帖子）。建议在实际开发中添加适当的错误响应，例如：
     - 帖子不存在：返回 404 状态码
     - 无权限：返回 403 状态码
