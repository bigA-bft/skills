---
name: hono
description: 如果需要使用Hono框架，可以使用这个技能来快速搭建一个简单的Web服务器。
---


## 使用 Zod验证
### 从 Npm 注册表安装。
```bash
npm i zod
```
### 从 zod 导入 z。
```bash
import * as z from 'zod'
```
### 编写你的模式。
```js
const schema = z.object({
  body: z.string(),
})
```

### 你可以在回调函数中使用模式进行验证并返回验证后的值。
```js
const route = app.post(
  '/posts',
  validator('form', (value, c) => {
    const parsed = schema.safeParse(value)
    if (!parsed.success) {
      return c.text('Invalid!', 401)
    }
    return parsed.data
  }),
  (c) => {
    const { body } = c.req.valid('form')
    // ... do something
    return c.json(
      {
        message: 'Created!',
      },
      201
    )
  }
)
```


## Zod 验证器中间件

### 你可以使用 Zod 验证器中间件 使其更加容易。
```bash
npm i @hono/zod-validator
```

### 并导入 zValidator。
```js
import { zValidator } from '@hono/zod-validator'
```

### 校验
```js
const route = app.post(
  '/posts',
  zValidator(
    'form',
    z.object({
      body: z.string(),
    })
  ),
  (c) => {
    const validated = c.req.valid('form')
    // ... use your validated data
  }
)
```