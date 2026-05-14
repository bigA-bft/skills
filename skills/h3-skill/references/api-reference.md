# h3 API 完整参考

## 应用创建

### createApp

创建一个 h3 应用实例。

```typescript
import { createApp } from 'h3'

const app = createApp({
  debug: true,              // 启用调试模式
  onError: (error) => {    // 全局错误处理
    console.error('App error:', error)
  },
  onRequest: (event) => {  // 每个请求的处理
    console.log('Request:', event.path)
  }
})
```

### toNodeListener

将 h3 应用转换为 Node.js HTTP 服务器监听器。

```typescript
import { createApp, toNodeListener } from 'h3'
import { createServer } from 'node:http'

const app = createApp()
const server = createServer(toNodeListener(app))
server.listen(3000)
```

### listen

快速启动一个 HTTP 服务器（开发便利函数）。

```typescript
import { createApp, listen } from 'h3'

const app = createApp()
await listen(app, { port: 3000, host: '0.0.0.0' })
console.log('Server running on http://localhost:3000')
```

## 事件处理器

### defineEventHandler

定义一个类型安全的事件处理器。

```typescript
import { defineEventHandler } from 'h3'

// 基础用法
const handler = defineEventHandler((event) => {
  return 'Hello'
})

// 带类型参数
interface User {
  id: number
  name: string
}

const handler = defineEventHandler<User>((event) => {
  return { id: 1, name: 'John' }
})

// 异步处理器
const handler = defineEventHandler(async (event) => {
  const data = await fetchData()
  return data
})
```

### defineLazyEventHandler

延迟加载处理器（用于代码分割）。

```typescript
import { defineLazyEventHandler } from 'h3'

const handler = defineLazyEventHandler(() => {
  return import('./heavy-handler').then(m => m.default)
})
```

### defineRequestMiddleware

定义请求中间件。

```typescript
import { defineRequestMiddleware } from 'h3'

const middleware = defineRequestMiddleware((event) => {
  console.log('Before handler')
  event.context.startTime = Date.now()
})
```

### defineResponseMiddleware

定义响应中间件。

```typescript
import { defineResponseMiddleware } from 'h3'

const middleware = defineResponseMiddleware((event) => {
  const duration = Date.now() - event.context.startTime
  console.log(`Request took ${duration}ms`)
})
```

## 请求工具

### URL 和查询参数

#### getQuery

获取 URL 查询参数（自动解析）。

```typescript
// /api/search?q=hello&page=1&tags=foo&tags=bar
const query = getQuery(event)
// { q: 'hello', page: '1', tags: ['foo', 'bar'] }

// 带默认值
const { q = '', page = '1' } = getQuery(event)
```

#### getQueryItem

获取单个查询参数（返回字符串而非数组）。

```typescript
const q = getQueryItem(event, 'q') // 'hello'
```

#### getRouterParam

获取路由参数。

```typescript
// 路由: /api/users/:id
const id = getRouterParam(event, 'id') // '123'

// 多段参数: /api/files/:path*
const path = getRouterParam(event, 'path') // 'a/b/c'
```

#### getRouterParams

获取所有路由参数。

```typescript
// /api/users/123/posts/456
const params = getRouterParams(event)
// { id: '123', postId: '456' }
```

#### getRequestURL

获取完整的请求 URL。

```typescript
const url = getRequestURL(event)
// URL { href: 'http://localhost:3000/api/users', ... }
```

#### getRequestHost

获取请求主机名。

```typescript
const host = getRequestHost(event) // 'api.example.com'
const hostWithPort = getRequestHost(event, 'x-forwarded-host') // 带端口
```

#### getRequestProtocol

获取请求协议。

```typescript
const protocol = getRequestProtocol(event) // 'https'
```

#### getRequestIP

获取客户端 IP 地址。

```typescript
const ip = getRequestIP(event) // '192.168.1.1'
const ip = getRequestIP(event, { xForwardedFor: true }) // 考虑代理头
```

#### getRequestFingerprint

获取请求指纹（用于标识）。

```typescript
const fingerprint = getRequestFingerprint(event, {
  ip: true,
  userAgent: true
})
```

### 请求头

#### getHeader / getHeaders

获取请求头。

```typescript
// 单个头（不区分大小写）
const auth = getHeader(event, 'authorization')

// 所有头
const headers = getHeaders(event)
```

#### getRequestHeader / getRequestHeaders

类型安全的请求头获取。

```typescript
const contentType = getRequestHeader(event, 'content-type')
const headers = getRequestHeaders(event)
```

#### getRequestWebStream

获取请求体的 Web Stream。

```typescript
const stream = getRequestWebStream(event)
```

### HTTP 方法

#### getMethod

获取 HTTP 方法。

```typescript
const method = getMethod(event) // 'GET', 'POST', etc.
```

#### isMethod

检查 HTTP 方法。

```typescript
if (isMethod(event, 'POST')) {
  // 处理 POST
}

if (isMethod(event, ['GET', 'HEAD'])) {
  // 处理 GET 或 HEAD
}
```

#### assertMethod

断言 HTTP 方法，不匹配时抛出错误。

```typescript
assertMethod(event, 'POST') // 非 POST 时抛出 405 错误
assertMethod(event, ['GET', 'HEAD'])
```

### 请求体解析

#### readBody

读取并解析请求体。

```typescript
// JSON
const body = await readBody(event)

// 带类型
interface UserInput {
  name: string
  email: string
}
const body = await readBody<UserInput>(event)

// 原始字符串
const text = await readBody(event, { strict: false })
```

#### readRawBody

读取原始请求体。

```typescript
const buffer = await readRawBody(event) // Buffer
const string = await readRawBody(event, 'utf8') // string
```

#### readFormData

读取为 FormData 对象。

```typescript
const form = await readFormData(event)
const name = form.get('name')
const file = form.get('file') as File
```

#### readMultipartFormData

读取 multipart/form-data（文件上传）。

```typescript
const parts = await readMultipartFormData(event)

for (const part of parts || []) {
  console.log(part.name)      // 字段名
  console.log(part.filename)  // 文件名（如果有）
  console.log(part.type)      // MIME 类型
  console.log(part.data)      // Buffer
}
```

#### readValidatedBody

带验证的 body 读取。

```typescript
import { z } from 'zod'

const schema = z.object({
  name: z.string(),
  age: z.number().optional()
})

const body = await readValidatedBody(event, schema.parse)
```

## 响应工具

### 发送响应

#### send

发送任意响应。

```typescript
await send(event, 'Hello World', 'text/plain')
await send(event, JSON.stringify(data), 'application/json')
```

#### sendNoContent

发送 204 No Content。

```typescript
return sendNoContent(event) // 默认 204
return sendNoContent(event, 205) // Reset Content
```

#### sendRedirect

发送重定向响应。

```typescript
return sendRedirect(event, '/new-path') // 默认 302
return sendRedirect(event, '/new-path', 301) // 永久重定向
return sendRedirect(event, '/new-path', 307) // 临时重定向（保持方法）
```

#### sendStream

发送流响应。

```typescript
import { createReadStream } from 'node:fs'

const stream = createReadStream('./file.txt')
return sendStream(event, stream)
```

#### sendIterable

发送可迭代对象。

```typescript
async function* generate() {
  yield 'Hello '
  yield 'World'
}

return sendIterable(event, generate())
```

#### sendWebResponse

发送 Web 标准 Response。

```typescript
const response = new Response('Hello', { status: 200 })
return sendWebResponse(event, response)
```

### 响应头

#### setResponseStatus

设置响应状态码。

```typescript
setResponseStatus(event, 201)
setResponseStatus(event, 404, 'Not Found')
```

#### setResponseHeader

设置单个响应头。

```typescript
setResponseHeader(event, 'X-Custom', 'value')
```

#### setResponseHeaders

设置多个响应头。

```typescript
setResponseHeaders(event, {
  'Cache-Control': 'no-cache',
  'X-Request-ID': 'abc123'
})
```

#### appendResponseHeader

追加响应头（用于多值头）。

```typescript
appendResponseHeader(event, 'Set-Cookie', 'token=abc')
appendResponseHeader(event, 'Set-Cookie', 'user=john')
```

#### defaultContentType

设置默认 Content-Type（仅在未设置时）。

```typescript
defaultContentType(event, 'application/json')
```

### 响应信息

#### getResponseStatus

获取当前响应状态码。

```typescript
const status = getResponseStatus(event) // 200
```

#### getResponseStatusText

获取当前响应状态文本。

```typescript
const text = getResponseStatusText(event) // 'OK'
```

#### getResponseHeader / getResponseHeaders

获取已设置的响应头。

```typescript
const header = getResponseHeader(event, 'content-type')
const headers = getResponseHeaders(event)
```

## Cookies

#### parseCookies

解析所有 cookies。

```typescript
const cookies = parseCookies(event)
// { token: 'abc123', user: 'john' }
```

#### getCookie

获取单个 cookie。

```typescript
const token = getCookie(event, 'token')
```

#### setCookie

设置 cookie。

```typescript
setCookie(event, 'token', 'abc123', {
  domain: '.example.com',
  expires: new Date('2025-01-01'),
  httpOnly: true,
  maxAge: 60 * 60 * 24 * 7, // 秒
  path: '/',
  sameSite: 'strict', // 'lax', 'none'
  secure: true
})
```

#### deleteCookie

删除 cookie。

```typescript
deleteCookie(event, 'token')
deleteCookie(event, 'token', { path: '/admin' })
```

## Session

需要先配置 session 密码。

#### getSession

获取会话数据。

```typescript
const session = await getSession(event)
// session 是一个对象，可以存储任意数据
```

#### updateSession

更新会话数据。

```typescript
await updateSession(event, { count: 1, userId: 123 })
```

#### sealSession

密封会话数据（手动创建会话 cookie）。

```typescript
const sealed = await sealSession(event, data)
```

#### unsealSession

解封会话数据。

```typescript
const data = await unsealSession(event, sealed)
```

#### clearSession

清除会话。

```typescript
await clearSession(event)
```

## 错误处理

#### createError

创建一个 H3Error。

```typescript
throw createError({
  statusCode: 404,
  statusMessage: 'Not Found',
  message: 'User not found',
  data: { userId: 123 },
  cause: originalError
})
```

#### isError

检查是否为 H3Error。

```typescript
if (isError(error)) {
  console.log(error.statusCode)
}
```

#### sendError

发送错误响应（通常由框架自动调用）。

```typescript
sendError(event, error)
```

## 代理请求

#### proxyRequest

代理请求到另一服务器。

```typescript
return proxyRequest(event, 'https://api.example.com')

// 带选项
return proxyRequest(event, 'https://api.example.com', {
  fetchOptions: {
    headers: {
      'Authorization': 'Bearer token'
    }
  },
  headers: {
    // 发送到客户端的响应头
    'cache-control': 'no-cache'
  },
  headersExclude: ['set-cookie'] // 排除的头
})
```

#### sendProxy

发送代理请求（更底层的控制）。

```typescript
return sendProxy(event, 'https://api.example.com')
```

## Web 标准 API

#### toWebRequest

转换为标准 Web Request。

```typescript
const request = toWebRequest(event)
// 现在可以使用标准 Web API
```

#### fromWebHandler

从标准 Web Handler 创建 h3 处理器。

```typescript
app.use(fromWebHandler((request) => {
  return new Response('Hello')
}))
```

## 工具函数

#### isStream

检查是否为流。

```typescript
if (isStream(data)) {
  return sendStream(event, data)
}
```

#### isReadableStream

检查是否为 ReadableStream。

```typescript
if (isReadableStream(data)) {
  // 处理 Web Stream
}
```

#### sanitizeStatusCode

清理状态码。

```typescript
const code = sanitizeStatusCode(200) // 200
const code = sanitizeStatusCode(999) // 200（默认值）
```

#### sanitizeStatusMessage

清理状态消息。

```typescript
const message = sanitizeStatusMessage('OK') // 'OK'
```

#### splitCookiesString

分割 Set-Cookie 头字符串。

```typescript
const cookies = splitCookiesString('a=b; c=d, e=f')
```

## 类型定义

### H3Event

事件对象类型。

```typescript
import type { H3Event } from 'h3'

function handler(event: H3Event) {
  // ...
}
```

### EventHandler

处理器类型。

```typescript
import type { EventHandler, EventHandlerRequest } from 'h3'

const handler: EventHandler = (event) => {
  return 'hello'
}

// 带请求类型
const handler: EventHandler<EventHandlerRequest<{ id: string }>> = (event) => {
  const id = getRouterParam(event, 'id')
  return { id }
}
```

### H3EventContext

上下文类型。

```typescript
import type { H3EventContext } from 'h3'

// 扩展上下文
declare module 'h3' {
  interface H3EventContext {
    user: { id: number; name: string }
  }
}
```

### 其他类型

```typescript
import type {
  H3Error,              // 错误类型
  HTTPMethod,           // HTTP 方法类型
  InferEventInput,      // 推断输入类型
  InferEventOutput,     // 推断输出类型
  MultiPartData,        //  multipart 数据类型
  SessionConfig,        // 会话配置类型
  Session,              // 会话数据类型
  AppOptions,           // 应用选项类型
  App,                  // 应用类型
  AppUse,               // use 方法类型
  NodeMiddleware,       // Node.js 中间件类型
  WebHandler            // Web Handler 类型
} from 'h3'
```

## 配置

### SessionConfig

会话配置。

```typescript
interface SessionConfig {
  name?: string              // cookie 名称，默认 'h3-session'
  password?: string          // 加密密码（至少32字符）
  cookie?: CookieSerializeOptions
  maxAge?: number           // 会话最大年龄（秒）
  sessionStore?: SessionStore
}
```

### AppOptions

应用配置。

```typescript
interface AppOptions {
  debug?: boolean           // 调试模式
  onError?: (error: H3Error, event: H3Event) => void | Promise<void>
  onRequest?: (event: H3Event) => void | Promise<void>
  onBeforeResponse?: (event: H3Event, response: { body?: unknown }) => void | Promise<void>
  onAfterResponse?: (event: H3Event, response: { body?: unknown }) => void | Promise<void>
}
```
