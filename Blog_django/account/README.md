# Account API 文档

本文档描述了 Django 项目中 Account 子应用的 API 接口，涵盖用户管理、身份验证和好友关系管理的功能。

## 身份验证

除部分公开接口外，大多数接口需要用户登录并提供 JWT 令牌进行身份验证。令牌需在请求头中以以下形式提供：

```
Authorization: Bearer <token>
```

以下接口无需身份验证：
- 用户注册 (`/signup/`)
- 用户登录 (`/login/`)
- 刷新令牌 (`/refresh/`)

## 接口列表

### 1. 用户注册

**接口名称**：用户注册  
**接口描述**：注册新用户并发送激活邮件。  
**请求方法**：POST  
**请求 URL**：`/signup/`  

#### 请求参数

| 参数名    | 类型   | 是否必填 | 描述       |
|-----------|--------|----------|------------|
| email     | string | 是       | 邮箱地址   |
| name      | string | 是       | 用户名     |
| password1 | string | 是       | 密码       |
| password2 | string | 是       | 确认密码   |

#### 返回参数

| 参数名  | 类型   | 描述           |
|---------|--------|----------------|
| message | string | 操作结果，成功返回 "success"，失败返回错误信息 |

#### 示例

**请求：**
```json
{
    "email": "example@example.com",
    "name": "example",
    "password1": "password123",
    "password2": "password123"
}
```

**响应（成功）：**
```json
{
    "message": "success"
}
```

**响应（失败，例如邮箱已存在）：**
```json
{
    "message": "{\"email\": [{\"message\": \"该邮箱已注册\", \"code\": \"unique\"}]}"
}
```

---

### 2. 获取当前用户信息

**接口名称**：获取当前用户信息  
**接口描述**：获取当前登录用户的基本信息。  
**请求方法**：GET  
**请求 URL**：`/me/`  

#### 请求参数
无

#### 返回参数

| 参数名 | 类型   | 描述       |
|--------|--------|------------|
| id     | string | 用户 ID    |
| name   | string | 用户名     |
| email  | string | 邮箱地址   |
| avatar | string | 头像 URL   |

#### 示例

**响应：**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "example",
    "email": "example@example.com",
    "avatar": "https://example.com/avatars/example.jpg"
}
```

---

### 3. 用户登录

**接口名称**：用户登录  
**接口描述**：用户登录并获取 JWT 令牌。  
**请求方法**：POST  
**请求 URL**：`/login/`  

#### 请求参数

| 参数名   | 类型   | 是否必填 | 描述     |
|----------|--------|----------|----------|
| email    | string | 是       | 邮箱地址 |
| password | string | 是       | 密码     |

#### 返回参数

| 参数名  | 类型   | 描述         |
|---------|--------|--------------|
| refresh | string | 刷新令牌     |
| access  | string | 访问令牌     |

#### 示例

**请求：**
```json
{
    "email": "example@example.com",
    "password": "password123"
}
```

**响应：**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 4. 刷新令牌

**接口名称**：刷新令牌  
**接口描述**：使用刷新令牌获取新的访问令牌。  
**请求方法**：POST  
**请求 URL**：`/refresh/`  

#### 请求参数

| 参数名  | 类型   | 是否必填 | 描述     |
|---------|--------|----------|----------|
| refresh | string | 是       | 刷新令牌 |

#### 返回参数

| 参数名 | 类型   | 描述     |
|--------|--------|----------|
| access | string | 新访问令牌 |

#### 示例

**请求：**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**响应：**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 5. 编辑用户资料

**接口名称**：编辑用户资料  
**接口描述**：编辑当前登录用户的资料，支持更新用户名和头像。  
**请求方法**：POST  
**请求 URL**：`/editprofile/`  

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述     |
|--------|--------|----------|----------|
| name   | string | 否       | 用户名   |
| avatar | file   | 否       | 头像文件 |

#### 返回参数

| 参数名  | 类型   | 描述             |
|---------|--------|------------------|
| message | string | 操作结果         |
| user    | object | 更新后的用户信息 |

**返回参数（user 对象）：**

| 参数名       | 类型   | 描述       |
|--------------|--------|------------|
| id           | string | 用户 ID    |
| name         | string | 用户名     |
| email        | string | 邮箱地址   |
| friends_count| int    | 好友数量   |
| posts_count  | int    | 帖子数量   |
| get_avatar   | string | 头像 URL   |

#### 示例

**请求（仅更新用户名）：**
```json
{
    "name": "new_name"
}
```

**响应：**
```json
{
    "message": "修改已更新",
    "user": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "new_name",
        "email": "example@example.com",
        "friends_count": 2,
        "posts_count": 5,
        "get_avatar": "https://example.com/avatars/example.jpg"
    }
}
```

---

### 6. 修改密码

**接口名称**：修改密码  
**接口描述**：修改当前登录用户的密码。  
**请求方法**：POST  
**请求 URL**：`/editpassword/`  

#### 请求参数

| 参数名        | 类型   | 是否必填 | 描述       |
|---------------|--------|----------|------------|
| old_password  | string | 是       | 旧密码     |
| new_password1 | string | 是       | 新密码     |
| new_password2 | string | 是       | 确认新密码 |

#### 返回参数

| 参数名  | 类型   | 描述           |
|---------|--------|----------------|
| message | string | 操作结果，成功返回 "success"，失败返回错误信息 |

#### 示例

**请求：**
```json
{
    "old_password": "old_password123",
    "new_password1": "new_password123",
    "new_password2": "new_password123"
}
```

**响应（成功）：**
```json
{
    "message": "success"
}
```

**响应（失败，例如旧密码错误）：**
```json
{
    "message": "{\"old_password\": [{\"message\": \"旧密码错误\", \"code\": \"invalid\"}]}"
}
```

---

### 7. 获取好友建议

**接口名称**：获取好友建议  
**接口描述**：获取当前登录用户可能认识的人的列表。  
**请求方法**：GET  
**请求 URL**：`/friends/suggested/`  

#### 请求参数
无

#### 返回参数

| 参数名 | 类型  | 描述           |
|--------|-------|----------------|
|        | array | 建议的好友列表 |

**返回参数（数组中每个对象）：**

| 参数名       | 类型   | 描述       |
|--------------|--------|------------|
| id           | string | 用户 ID    |
| name         | string | 用户名     |
| email        | string | 邮箱地址   |
| friends_count| int    | 好友数量   |
| posts_count  | int    | 帖子数量   |
| get_avatar   | string | 头像 URL   |

#### 示例

**响应：**
```json
[
    {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "friend1",
        "email": "friend1@example.com",
        "friends_count": 10,
        "posts_count": 20,
        "get_avatar": "https://example.com/avatars/friend1.jpg"
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "name": "friend2",
        "email": "friend2@example.com",
        "friends_count": 5,
        "posts_count": 15,
        "get_avatar": "https://example.com/avatars/friend2.jpg"
    }
]
```

---

### 8. 获取用户好友列表

**接口名称**：获取用户好友列表  
**接口描述**：获取指定用户的好友列表，若为当前用户，则额外返回收到的好友请求。  
**请求方法**：GET  
**请求 URL**：`/friends/<uuid:pk>/`  

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述     |
|--------|------|----------|----------|
| pk     | uuid | 是       | 用户 ID  |

#### 返回参数

| 参数名   | 类型  | 描述           |
|----------|-------|----------------|
| user     | object| 用户信息       |
| friends  | array | 好友列表       |
| requests | array | 好友请求列表（仅当 pk 为当前用户时返回） |

**返回参数（user 对象）：**

| 参数名       | 类型   | 描述       |
|--------------|--------|------------|
| id           | string | 用户 ID    |
| name         | string | 用户名     |
| email        | string | 邮箱地址   |
| friends_count| int    | 好友数量   |
| posts_count  | int    | 帖子数量   |
| get_avatar   | string | 头像 URL   |

**返回参数（friends 数组中每个对象）：**

| 参数名       | 类型   | 描述       |
|--------------|--------|------------|
| id           | string | 用户 ID    |
| name         | string | 用户名     |
| email        | string | 邮箱地址   |
| friends_count| int    | 好友数量   |
| posts_count  | int    | 帖子数量   |
| get_avatar   | string | 头像 URL   |

**返回参数（requests 数组中每个对象）：**

| 参数名    | 类型   | 描述           |
|-----------|--------|----------------|
| id        | string | 请求 ID        |
| created_by| object | 发起请求的用户信息 |

#### 示例

**响应（当前用户）：**
```json
{
    "user": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "example",
        "email": "example@example.com",
        "friends_count": 2,
        "posts_count": 5,
        "get_avatar": "https://example.com/avatars/example.jpg"
    },
    "friends": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "friend1",
            "email": "friend1@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/friend1.jpg"
        }
    ],
    "requests": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "created_by": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "name": "requester",
                "email": "requester@example.com",
                "friends_count": 3,
                "posts_count": 7,
                "get_avatar": "https://example.com/avatars/requester.jpg"
            }
        }
    ]
}
```

---

### 9. 发送好友请求

**接口名称**：发送好友请求  
**接口描述**：向指定用户发送好友请求并创建通知。  
**请求方法**：POST  
**请求 URL**：`/friends/<uuid:pk>/request/`  

#### 请求参数

| 参数名 | 类型 | 是否必填 | 描述     |
|--------|------|----------|----------|
| pk     | uuid | 是       | 用户 ID  |

#### 返回参数

| 参数名  | 类型   | 描述     |
|---------|--------|----------|
| message | string | 操作结果 |

#### 示例

**响应：**
```json
{
    "message": "Friendship request sent successfully."
}
```

**响应（重复请求）：**
```json
{
    "message": "You have already sent a friendship request to this user."
}
```

---

### 10. 处理好友请求

**接口名称**：处理好友请求  
**接口描述**：处理从指定用户发送来的好友请求，支持接受或拒绝。  
**请求方法**：POST  
**请求 URL**：`/friends/<uuid:pk>/<str:status>/`  

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述                     |
|--------|--------|----------|--------------------------|
| pk     | uuid   | 是       | 发送请求的用户 ID        |
| status | string | 是       | 请求状态（accepted 或 rejected） |

#### 返回参数

| 参数名  | 类型   | 描述     |
|---------|--------|----------|
| message | string | 操作结果 |

#### 示例

**响应：**
```json
{
    "message": "friendship request updated"
}
```

---

## 注意事项

1. **数据格式**：所有接口返回的数据均为 JSON 格式。
2. **错误处理**：表单验证失败时，返回的 `message` 字段将包含详细错误信息，格式为 JSON 字符串。
3. **文件上传**：`/editprofile/` 接口支持上传头像文件，需使用 `multipart/form-data` 格式。
4. **URL 参数**：部分接口使用路径参数（如 `pk` 和 `status`），需正确传递。
5. **通知机制**：发送和处理好友请求时会生成通知，但通知内容不在返回数据中。
