---
name: h3-skill
description: h3 是一个最小化、高性能的 JavaScript/TypeScript HTTP 框架，由 UnJS 团队创建。它是运行时无关的，可在 Node.js、Deno、Bun、Cloudflare Workers 等边缘运行时上运行。使用场景：(1) 使用 h3 创建 HTTP 服务器和 API，(2) 开发基于 Nitro 或 Nuxt 3 的服务端功能，(3) 编写事件处理器 (event handlers)，(4) 处理请求/响应对象，(5) 使用中间件模式，(6) 创建跨平台的 Web 应用，(7) 使用 Web 标准 API，(8) 处理流和 Server-Sent Events。
---

# h3 开发指南

## 概述

h3 是一个最小化、高性能的 HTTP 框架，由 [UnJS](https://unjs.io) 团队创建。它是 Nitro 和 Nuxt 3 的底层基础。

**核心特点：**
- 运行时无关：支持 Node.js、Deno、Bun、Cloudflare Workers
- 基于 Web 标准：使用原生 `Request`/`Response` API
- 高性能：最小化开销，优化的请求处理
- TypeScript 优先：完整的类型支持

## 快速开始

### 独立使用

```typescript
import { createApp, defineEventHandler, toNodeListener } from 'h3'
import { createServer } from 'node:http'

const app = createApp()

app.use('/', defineEventHandler(() => {
  return { message: 'Hello from h3!' }
}))

createServer(toNodeListener(app)).listen(3000)
```

### 使用 listen 快捷方式

```typescript
import { createApp, defineEventHandler, listen } from 'h3'

const app = createApp()

app.use('/api/hello', defineEventHandler((event) => {
  const name = getQuery(event).name || 'World'
  return { message: `Hello ${name}!` }
}))

listen(app, { port: 3000 })
```

## 核心概念

### 事件处理器 (Event Handlers)

```typescript
import { defineEventHandler, defineLazyEventHandler } from 'h3'

// 标准处理器
const handler = defineEventHandler((event) => {
  return { status: 'ok' }
})

// 延迟加载处理器（用于代码分割）
const lazyHandler = defineLazyEventHandler(() => {
  return import('./heavy-handler').then(m => m.default)
})
```

### H3Event 对象

```typescript
event.node          // Node.js req/res (仅在 Node 环境)
event.context       // 共享上下文对象
event.path          // 请求路径
event.method        // HTTP 方法（大写）
event.headers       // 请求头（标准化）
```

## 请求处理

### 查询参数

```typescript
// GET /api/search?q=hello&page=1
export default defineEventHandler((event) => {
  const query = getQuery(event)
  // query = { q: 'hello', page: '1' }

  const { q, page = '1' } = getQuery(event)
  return { search: q, page: Number(page) }
})
```

### 路由参数

```typescript
// 文件: server/api/users/[id].get.ts
export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id')
  // 或获取所有参数
  const params = getRouterParams(event)
  return { userId: id }
})

// 多段参数: server/api/files/[...path].ts
export default defineEventHandler((event) => {
  const path = getRouterParam(event, 'path') // "a/b/c"
  return { filePath: path }
})
```

### 请求头

```typescript
export default defineEventHandler((event) => {
  // 获取单个头（不区分大小写）
  const auth = getHeader(event, 'authorization')

  // 获取所有头
  const headers = getHeaders(event)

  // 类型安全的获取
  const contentType = getRequestHeader(event, 'content-type')

  return { auth, contentType }
})
```

### 请求体

```typescript
// JSON 请求体
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  // body 会被自动解析为对象
  return { received: body }
})

// 带类型
interface UserInput {
  name: string
  email: string
}

export default defineEventHandler(async (event) => {
  const body = await readBody<UserInput>(event)
  return { user: body }
})
```

### 表单数据

```typescript
// application/x-www-form-urlencoded
export default defineEventHandler(async (event) => {
  const form = await readFormData(event)
  const name = form.get('name')
  return { name }
})

// multipart/form-data（文件上传）
export default defineEventHandler(async (event) => {
  const formData = await readMultipartFormData(event)

  const file = formData?.find(item => item.name === 'file')
  if (!file) {
    throw createError({ statusCode: 400, message: 'No file uploaded' })
  }

  // file.data - Buffer
  // file.filename - 原始文件名
  // file.type - MIME 类型

  await writeFile(`./uploads/${file.filename}`, file.data)

  return {
    filename: file.filename,
    size: file.data.length,
    type: file.type
  }
})
```

### 验证请求体

```typescript
import { z } from 'zod'

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().optional()
})

export default defineEventHandler(async (event) => {
  const body = await readValidatedBody(event, userSchema.parse)
  // body 已被验证且类型正确
  return { validUser: body }
})
```

## 响应处理

### 基础响应

```typescript
// 自动 JSON 序列化
export default defineEventHandler(() => {
  return { status: 'ok', data: [] }
})

// 原始响应
export default defineEventHandler((event) => {
  return send(event, 'Hello World', 'text/plain')
})

// 空响应
export default defineEventHandler((event) => {
  return sendNoContent(event, 204)
})
```

### 状态码和头

```typescript
export default defineEventHandler((event) => {
  setResponseStatus(event, 201)
  setResponseHeader(event, 'X-Custom-Header', 'value')
  setResponseHeaders(event, {
    'Cache-Control': 'no-cache',
    'X-Request-ID': generateId()
  })

  return { created: true }
})
```

### 重定向

```typescript
export default defineEventHandler((event) => {
  return sendRedirect(event, '/new-path', 301) // 永久重定向
  // 或 302 临时重定向
})
```

### 流响应

```typescript
import { createReadStream } from 'node:fs'

export default defineEventHandler((event) => {
  const stream = createReadStream('./large-file.txt')
  return sendStream(event, stream)
})

// Server-Sent Events
export default defineEventHandler((event) => {
  setResponseHeader(event, 'Content-Type', 'text/event-stream')
  setResponseHeader(event, 'Cache-Control', 'no-cache')
  setResponseHeader(event, 'Connection', 'keep-alive')

  const stream = new ReadableStream({
    start(controller) {
      let count = 0
      const interval = setInterval(() => {
        count++
        controller.enqueue(`data: ${JSON.stringify({ time: Date.now(), count })}\n\n`)

        if (count >= 10) {
          clearInterval(interval)
          controller.close()
        }
      }, 1000)

      event.node.req.on('close', () => {
        clearInterval(interval)
      })
    }
  })

  return sendStream(event, stream)
})
```

## Cookies

```typescript
export default defineEventHandler((event) => {
  // 读取 cookie
  const token = getCookie(event, 'token')
  const allCookies = parseCookies(event)

  // 设置 cookie
  setCookie(event, 'token', 'abc123', {
    httpOnly: true,
    secure: true,
    maxAge: 60 * 60 * 24 * 7, // 7天
    path: '/',
    sameSite: 'strict'
  })

  // 删除 cookie
  deleteCookie(event, 'token')

  return { token }
})
```

## 会话 (Session)

```typescript
// 需要先配置 session 密码（在 nitro.config.ts 中）
export default defineNitroConfig({
  session: {
    name: 'nuxt-session',
    password: process.env.SESSION_PASSWORD // 至少32字符
  }
})

// 使用会话
export default defineEventHandler(async (event) => {
  // 获取会话
  const session = await getSession(event)

  // 更新会话数据
  session.count = (session.count || 0) + 1
  session.lastVisit = new Date().toISOString()

  await updateSession(event, session)

  return {
    visitCount: session.count,
    lastVisit: session.lastVisit
  }
})
```

## 错误处理

```typescript
// 创建错误
export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id')
  const user = findUser(id)

  if (!user) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Not Found',
      message: `User with id ${id} not found`
    })
  }

  return user
})

// 自定义错误处理
export default defineEventHandler(async (event) => {
  try {
    const data = await fetchData()
    return data
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch data',
      cause: error
    })
  }
})
```

## 中间件

### 基础中间件

```typescript
// server/middleware/auth.ts
export default defineEventHandler((event) => {
  // 跳过某些路径
  if (event.path.startsWith('/api/public')) {
    return
  }

  const token = getHeader(event, 'authorization')

  if (!token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized'
    })
  }

  // 存储到上下文
  event.context.user = verifyToken(token)
})
```

### 日志中间件

```typescript
// server/middleware/log.ts
export default defineEventHandler((event) => {
  const start = Date.now()

  event.context.startTime = start

  event.node.res.on('finish', () => {
    const duration = Date.now() - start
    console.log(`${event.method} ${event.path} - ${event.node.res.statusCode} - ${duration}ms`)
  })
})
```

### 顺序执行

中间件按照文件名字母顺序执行。可以用数字前缀控制顺序：

```
server/middleware/
  01.logger.ts    # 先执行
  02.auth.ts      # 后执行
```

## Nitro/Nuxt 3 集成

### API 路由

```typescript
// server/api/users.get.ts - 处理 GET /api/users
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  return await fetchUsers(query)
})

// server/api/users.post.ts - 处理 POST /api/users
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  return await createUser(body)
})

// server/api/users/[id].get.ts - 处理 GET /api/users/:id
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  return await fetchUserById(id)
})

// server/api/users/[id].put.ts - 处理 PUT /api/users/:id
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  const body = await readBody(event)
  return await updateUser(id, body)
})

// server/api/users/[id].delete.ts - 处理 DELETE /api/users/:id
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  await deleteUser(id)
  return { success: true }
})
```

### 工具函数

```typescript
// server/utils/db.ts
export const db = createDatabase()

// server/utils/response.ts
export function createApiResponse<T>(data: T, message = 'success') {
  return {
    code: 0,
    message,
    data,
    timestamp: Date.now()
  }
}

export function createApiError(message: string, code = 1, statusCode = 400) {
  throw createError({
    statusCode,
    message,
    data: { code }
  })
}
```

## 常见模式

### CORS 处理

```typescript
// server/middleware/cors.ts
export default defineEventHandler((event) => {
  setResponseHeaders(event, {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
  })

  if (getMethod(event) === 'OPTIONS') {
    return null
  }
})
```

### API 版本控制

```typescript
// server/api/v1/users.ts
export default defineEventHandler(() => {
  return { version: 'v1', users: [] }
})

// server/api/v2/users.ts
export default defineEventHandler(() => {
  return { version: 'v2', users: [], meta: {} }
})
```

### 速率限制

```typescript
// server/middleware/rate-limit.ts
const requests = new Map<string, { count: number; resetTime: number }>()

export default defineEventHandler((event) => {
  const ip = getRequestIP(event) || 'unknown'
  const now = Date.now()
  const windowMs = 60 * 1000 // 1分钟
  const maxRequests = 100

  const record = requests.get(ip)

  if (!record || now > record.resetTime) {
    requests.set(ip, { count: 1, resetTime: now + windowMs })
  } else {
    record.count++
    if (record.count > maxRequests) {
      throw createError({
        statusCode: 429,
        message: 'Too many requests'
      })
    }
  }
})
```

### 代理请求

```typescript
import { proxyRequest } from 'h3'

export default defineEventHandler(async (event) => {
  const target = 'https://api.example.com'

  return proxyRequest(event, target, {
    fetchOptions: {
      headers: {
        'Authorization': `Bearer ${process.env.API_TOKEN}`
      }
    }
  })
})
```

### Webhook 处理

```typescript
export default defineEventHandler(async (event) => {
  const signature = getHeader(event, 'x-webhook-signature')
  const body = await readRawBody(event)

  // 验证签名
  if (!verifySignature(body, signature)) {
    throw createError({ statusCode: 401, message: 'Invalid signature' })
  }

  const payload = JSON.parse(body)

  // 处理 webhook
  await processWebhook(payload)

  return { received: true }
})
```

## Web 标准 API

```typescript
import { toWebRequest, fromWebHandler } from 'h3'

// 转换为标准 Web Request
export default defineEventHandler((event) => {
  const request = toWebRequest(event)
  // 现在可以使用标准 Web API
})

// 使用标准 Web Handler
app.use(fromWebHandler((request) => {
  return new Response('Hello from Web API')
}))
```

## 参考资料

- [完整 API 参考](references/api-reference.md) - 所有工具函数的详细说明
- [Nitro 文档](https://nitro.unjs.io/) - 上层框架文档
- [Nuxt 3 服务端](https://nuxt.com/docs/guide/directory-structure/server) - Nuxt 3 中使用 h3
