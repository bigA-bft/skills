---
name: vue3-skill
description: Vue3 + TypeScript + Vite 前端开发技能。用于组件开发、页面创建、代码规范检查。触发场景：(1) 创建 Vue3 组件，(2) 创建 Vue3 页面，(3) 使用 Vue3 组合式 API，(4) Vue3 + TypeScript 开发，(5) Vite 项目开发。
---

# Vue3 + TypeScript + Vite 开发技能

## 核心原则

- 使用 **Composition API** (`<script setup>` 语法)
- 优先使用 **TypeScript**，定义清晰的类型
- 组件命名使用 PascalCase
- Props 使用 `defineProps` 并明确类型
- Emits 使用 `defineEmits` 并明确事件类型

## 快速开始

### 创建组件

复制 `assets/component-template/` 下的模板到目标目录：

```
components/
├── MyComponent.vue      # 主组件文件
├── types.ts             # 类型定义（可选）
└── index.ts             # 导出文件
```

### 创建页面

复制 `assets/page-template/` 下的模板到目标目录：

```
pages/
├── MyPage.vue           # 页面组件
├── composables/         # 页面专用组合式函数
│   └── usePageLogic.ts
└── types.ts             # 页面类型定义
```

## 代码规范

详细规范参考 [references/vue3-style-guide.md](references/vue3-style-guide.md)

### 组件结构规范

```vue
<script setup lang="ts">
// 1. 类型导入
import type { PropType } from 'vue'

// 2. 组件/工具导入
import { ref, computed } from 'vue'
import ChildComponent from './ChildComponent.vue'

// 3. 类型定义
interface User {
  id: number
  name: string
}

// 4. Props 定义
const props = defineProps<{
  title: string
  user?: User
}>()

// 5. Emits 定义
const emit = defineEmits<{
  submit: [data: User]
  cancel: []
}>()

// 6. 响应式状态
const count = ref(0)
const userList = ref<User[]>([])

// 7. 计算属性
const doubleCount = computed(() => count.value * 2)

// 8. 方法
const handleSubmit = () => {
  emit('submit', { id: 1, name: 'test' })
}
</script>

<template>
  <div class="my-component">
    <h1>{{ title }}</h1>
    <ChildComponent :count="doubleCount" />
    <button @click="handleSubmit">提交</button>
  </div>
</template>

<style scoped>
.my-component {
  padding: 16px;
}
</style>
```

## 常用模式

### Props 默认值

```vue
<script setup lang="ts">
interface Props {
  title?: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '默认标题',
  count: 0
})
</script>
```

### 使用 composable 提取逻辑

```ts
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initial = 0) {
  const count = ref(initial)
  const double = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  return { count, double, increment }
}
```

### 异步数据获取

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const data = ref<DataType | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.getData()
    data.value = res
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>
```

## 类型定义最佳实践

- 复用类型提取到 `types.ts` 文件
- API 返回类型统一在 `api/types.ts` 定义
- 组件 Props 类型直接在组件内定义，除非需要复用

## 模板参考

- 组件模板：`assets/component-template/`
- 页面模板：`assets/page-template/`


## api.openapi文档
参考./references/api.openapi.json

## api使用示例
```js
var myHeaders = new Headers();
myHeaders.append("Authorization", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NTczMDkwMDMwMDUsInBheWxvYWQiOiJ7XCJhcHBcIjpcInY3MjBcIixcInVzZXJJZFwiOlwiYjJiZTA5NjRiNWZkMzk2NGNkMTEzN2M5Y2IwOGI5ZDhcIn0ifQ.sAjPuZjUyMNvPCNptBmTEwoUU9nOZe-KJstVaFiXrKU");
myHeaders.append("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "*/*");
myHeaders.append("Host", "v720.naxclow.com");
myHeaders.append("Connection", "keep-alive");

var raw = "";

var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};

fetch("https://v720.naxclow.com/app/api/ApiSysDevices/getDevicesList", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```