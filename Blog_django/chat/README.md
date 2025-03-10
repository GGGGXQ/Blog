# Chat API 文档

本文档描述了 Django 项目中 Chat 子应用的 API 接口，涵盖对话管理、消息发送等功能。以下接口基于提供的代码实现，并确保与代码逻辑一致。

## 身份验证

所有接口均需要用户登录并提供 JWT 令牌进行身份验证。令牌需在请求头中以以下形式提供：

```
Authorization: Bearer <token>
```

## 接口列表

### 1. 获取对话列表

**接口名称**：获取对话列表  
**接口描述**：获取当前用户参与的所有对话列表。  
**请求方法**：GET  
**请求 URL**：`/`  

#### 请求参数
无

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
|                       | array  | 对话列表              |

**返回参数（数组中每个对象）：**

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 对话 ID（UUID 格式）  |
| users                 | array  | 参与对话的用户列表    |
| modified_at_formatted | string | 最后修改时间的格式化字符串（如 "1天前"） |

**用户对象（users 数组中每个对象）：**

| 参数名        | 类型   | 描述                  |
|---------------|--------|-----------------------|
| id            | string | 用户 ID（UUID 格式）  |
| name          | string | 用户名                |
| email         | string | 用户邮箱              |
| friends_count | int    | 好友数量              |
| posts_count   | int    | 帖子数量              |
| get_avatar    | string | 用户头像 URL          |

#### 示例

**响应：**
```json
[
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "users": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "user1",
                "email": "user1@example.com",
                "friends_count": 10,
                "posts_count": 20,
                "get_avatar": "https://example.com/avatars/user1.jpg"
            },
            {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "name": "user2",
                "email": "user2@example.com",
                "friends_count": 5,
                "posts_count": 15,
                "get_avatar": "https://example.com/avatars/user2.jpg"
            }
        ],
        "modified_at_formatted": "1天前"
    }
]
```

---

### 2. 获取对话详情

**接口名称**：获取对话详情  
**接口描述**：获取指定对话的详细信息，包括消息列表。  
**请求方法**：GET  
**请求 URL**：`/<uuid:pk>/`  

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述        |
|--------|------|----------|-------------|
| pk     | uuid | 是       | 对话 ID     |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 对话 ID（UUID 格式）  |
| users                 | array  | 参与对话的用户列表    |
| modified_at_formatted | string | 最后修改时间的格式化字符串（如 "1天前"） |
| messages              | array  | 消息列表              |

**消息对象（messages 数组中每个对象）：**

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 消息 ID（UUID 格式）  |
| sent_to               | object | 接收者用户信息        |
| created_by            | object | 发送者用户信息        |
| created_at_formatted  | string | 创建时间的格式化字符串（如 "1小时前"） |
| body                  | string | 消息内容              |

#### 示例

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "users": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "user1",
            "email": "user1@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/user1.jpg"
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "name": "user2",
            "email": "user2@example.com",
            "friends_count": 5,
            "posts_count": 15,
            "get_avatar": "https://example.com/avatars/user2.jpg"
        }
    ],
    "modified_at_formatted": "1天前",
    "messages": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "sent_to": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "name": "user2",
                "email": "user2@example.com",
                "friends_count": 5,
                "posts_count": 15,
                "get_avatar": "https://example.com/avatars/user2.jpg"
            },
            "created_by": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "user1",
                "email": "user1@example.com",
                "friends_count": 10,
                "posts_count": 20,
                "get_avatar": "https://example.com/avatars/user1.jpg"
            },
            "created_at_formatted": "1小时前",
            "body": "Hello, how are you?"
        }
    ]
}
```

---

### 3. 获取或创建对话

**接口名称**：获取或创建对话  
**接口描述**：获取与指定用户的对话，如果不存在则创建新的对话。  
**请求方法**：GET  
**请求 URL**：`/<uuid:user_pk>/get-or-create/`  

#### 请求参数

| 参数名  | 类型 | 是否必填 | 描述        |
|---------|------|----------|-------------|
| user_pk | uuid | 是       | 用户 ID     |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 对话 ID（UUID 格式）  |
| users                 | array  | 参与对话的用户列表    |
| modified_at_formatted | string | 最后修改时间的格式化字符串（如 "1天前"） |
| messages              | array  | 消息列表              |

#### 示例

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "users": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "user1",
            "email": "user1@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/user1.jpg"
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "name": "user2",
            "email": "user2@example.com",
            "friends_count": 5,
            "posts_count": 15,
            "get_avatar": "https://example.com/avatars/user2.jpg"
        }
    ],
    "modified_at_formatted": "1天前",
    "messages": []
}
```

---

### 4. 发送消息

**接口名称**：发送消息  
**接口描述**：向指定对话发送消息。  
**请求方法**：POST  
**请求 URL**：`/<uuid:pk>/send/`  

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述        |
|--------|--------|----------|-------------|
| pk     | uuid   | 是       | 对话 ID     |
| body   | string | 是       | 消息内容    |

#### 返回参数

| 参数名                | 类型   | 描述                  |
|-----------------------|--------|-----------------------|
| id                    | string | 消息 ID（UUID 格式）  |
| sent_to               | object | 接收者用户信息        |
| created_by            | object | 发送者用户信息        |
| created_at_formatted  | string | 创建时间的格式化字符串（如 "1小时前"） |
| body                  | string | 消息内容              |

#### 示例

**请求：**
```json
{
    "body": "Hello, how are you?"
}
```

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174003",
    "sent_to": {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "name": "user2",
        "email": "user2@example.com",
        "friends_count": 5,
        "posts_count": 15,
        "get_avatar": "https://example.com/avatars/user2.jpg"
    },
    "created_by": {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "user1",
        "email": "user1@example.com",
        "friends_count": 10,
        "posts_count": 20,
        "get_avatar": "https://example.com/avatars/user1.jpg"
    },
    "created_at_formatted": "1小时前",
    "body": "Hello, how are you?"
}
```

---

## 注意事项

1. **数据格式**：所有接口返回的数据均为 JSON 格式。
2. **身份验证**：接口依赖 Django REST Framework 的身份验证机制，确保 `request.user` 为已登录用户。
3. **时间格式**：`modified_at_formatted` 和 `created_at_formatted` 字段使用 `django.utils.timesince` 格式化，并翻译为中文（如 "1天前"、"1小时前"）。
4. **用户列表**：对话中的用户列表包含所有参与对话的用户信息，来源于 `UserSerializers`。
5. **消息发送**：发送消息时，系统自动将接收者设置为对话中除发送者外的唯一用户（适用于两人对话）。
6. **错误处理**：当前代码未显式处理异常（如对话不存在或用户无权限），实际开发中应添加适当的错误响应。