# Search API 接口文档

## 概述

`search` 子应用提供了一个搜索接口，允许用户通过关键字搜索其他用户和帖子。搜索结果包括与查询相关的用户列表和帖子列表，帖子的可见性根据隐私设置和用户关系进行过滤。

## 身份验证

该接口需要用户登录并提供身份验证。身份验证通过 JWT 令牌实现，用户需在请求头中提供令牌，格式如下：

```
Authorization: Bearer <token>
```

未提供有效令牌的请求将被拒绝。

---

## 接口详情

### 1. 搜索用户和帖子

#### 接口名称
搜索用户和帖子

#### 接口描述
根据提供的查询关键字搜索用户和帖子。用户搜索基于用户名，帖子搜索基于帖子内容，并考虑帖子的隐私设置和用户关系。

#### 请求方法
`POST`

#### 请求 URL
`/`

#### 请求参数

| 参数名 | 类型   | 是否必填 | 描述           |
|--------|--------|----------|----------------|
| query  | string | 是       | 搜索关键字     |

#### 返回参数

| 参数名 | 类型  | 描述       |
|--------|-------|------------|
| users  | array | 用户列表   |
| posts  | array | 帖子列表   |

**返回参数（users 数组中每个对象）：**

| 参数名        | 类型   | 描述                  |
|---------------|--------|-----------------------|
| id            | string | 用户 ID（UUID 格式）  |
| name          | string | 用户名                |
| email         | string | 用户邮箱              |
| friends_count | int    | 好友数量              |
| posts_count   | int    | 帖子数量              |
| get_avatar    | string | 用户头像 URL          |

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

#### 示例

**请求：**
```
POST /
Authorization: Bearer <token>
Content-Type: application/json

{
    "query": "example"
}
```

**响应：**
```json
{
    "users": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "example_user",
            "email": "example_user@example.com",
            "friends_count": 10,
            "posts_count": 20,
            "get_avatar": "https://example.com/avatars/example_user.jpg"
        }
    ],
    "posts": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "body": "This is an example post",
            "is_private": false,
            "likes_count": 10,
            "comments_count": 5,
            "is_liked": true,
            "created_by": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "example_user",
                "email": "example_user@example.com",
                "friends_count": 10,
                "posts_count": 20,
                "get_avatar": "https://example.com/avatars/example_user.jpg"
            },
            "created_at_formatted": "1天前",
            "attachments": []
        }
    ]
}
```

---

## 注意事项

1. **数据格式**  
   所有接口返回的数据均为 JSON 格式。

2. **搜索逻辑**  
   - **用户搜索**：基于用户名的模糊匹配（不区分大小写）。
   - **帖子搜索**：
     - 对于非私密帖子（`is_private=False`），搜索所有内容中包含查询关键字的帖子。
     - 对于私密帖子，只搜索当前用户及其好友创建的帖子中内容包含查询关键字的帖子。

3. **身份验证**  
   搜索接口需要用户登录，搜索结果会根据当前用户的身份和关系进行过滤。

4. **错误处理**  
   当前代码未显式处理异常情况（如查询参数缺失）。建议在实际开发中添加适当的错误响应，例如：
     - 查询参数缺失：返回 400 状态码。