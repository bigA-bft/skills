# Vue3 + TypeScript 开发规范

## 目录

1. [组件规范](#组件规范)
2. [TypeScript 规范](#typescript-规范)
3. [命名规范](#命名规范)
4. [代码组织](#代码组织)
5. [性能优化](#性能优化)

## 组件规范

### 使用 `<script setup>` 语法

```vue
<!-- 推荐 -->
<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
</script>

<!-- 不推荐 -->
<script lang="ts">
import { defineComponent, ref } from 'vue'
export default defineComponent({
  setup() {
    const count = ref(0)
    return { count }
  }
})
</script>
```

### Props 定义

```vue
<script setup lang="ts">
// 方式1: 简单类型
const props = defineProps<{
  title: string
  count: number
}>()

// 方式2: 带默认值
interface Props {
  title?: string
  count?: number
}
const props = withDefaults(defineProps<Props>(), {
  title: '默认值',
  count: 0
})

// 方式3: 复杂类型
import type { PropType } from 'vue'
const props = defineProps({
  user: Object as PropType<User>,
  tags: Array as PropType<string[]>
})
</script>
```

### Emits 定义

```vue
<script setup lang="ts">
// 推荐：严格类型定义
const emit = defineEmits<{
  submit: [data: FormData]
  cancel: []
  update: [value: string, oldValue: string]
}>()

// 使用
emit('submit', formData)
emit('cancel')
</script>
```

## TypeScript 规范

### 类型定义位置

```
src/
├── components/
│   ├── UserCard.vue
│   └── types.ts          # 组件共享类型
├── api/
│   └── types.ts          # API 相关类型
├── types/                # 全局类型
│   ├── global.d.ts
│   └── components.d.ts
```

### 接口命名

```ts
// 接口使用 PascalCase
interface UserInfo {
  id: number
  name: string
}

// 类型别名使用 PascalCase
type UserRole = 'admin' | 'user' | 'guest'

// Props 接口以 Props 结尾
interface ButtonProps {
  type: 'primary' | 'secondary'
}
```

### ref 类型推断

```ts
import { ref } from 'vue'

// 简单类型自动推断
const count = ref(0)           // Ref<number>
const message = ref('hello')   // Ref<string>

// 复杂类型显式声明
const user = ref<User | null>(null)
const list = ref<User[]>([])
```

## 命名规范

### 文件命名

| 类型 | 命名方式 | 示例 |
|------|---------|------|
| 组件 | PascalCase | `UserCard.vue` |
| 组合式函数 | camelCase 前缀 use | `useUser.ts` |
| 工具函数 | camelCase | `formatDate.ts` |
| 类型文件 | camelCase | `types.ts` |
| 常量文件 | camelCase | `constants.ts` |

### 组件命名

```vue
<!-- 单文件组件：PascalCase -->
<UserProfile />
<UserCard />

<!-- 在模板中使用 kebab-case 也可以 -->
<user-profile />
```

### 变量命名

```ts
// ref: 名词或形容词+名词
const user = ref(null)
const isLoading = ref(false)
const userList = ref([])

// computed: 形容词+名词 或 动词过去分词
const isValid = computed(() => ...)
const formattedDate = computed(() => ...)

// 方法: 动词+名词
const fetchUser = () => ...
const handleSubmit = () => ...
const updateCount = () => ...
```

## 代码组织

### 组件内顺序

```vue
<script setup lang="ts">
// 1. 导入
import type { ... } from '...'
import { ... } from 'vue'
import Component from './Component.vue'

// 2. 类型定义
interface Props { ... }
interface Emits { ... }

// 3. Props / Emits
const props = defineProps<...>()
const emit = defineEmits<...>()

// 4. 响应式状态
const state = ref(...)

// 5. 计算属性
const computed = computed(() => ...)

// 6. 监听
watch(...)

// 7. 生命周期
onMounted(() => ...)

// 8. 方法
const method = () => ...
</script>

<template>...\u003c/template>

<style scoped>...</style>
```

### 逻辑提取

```ts
// composables/usePagination.ts
import { ref, computed } from 'vue'

export function usePagination(total = 0, pageSize = 10) {
  const currentPage = ref(1)
  const totalPages = computed(() => Math.ceil(total / pageSize))

  const next = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  return {
    currentPage,
    totalPages,
    next
  }
}
```

## 性能优化

### 避免不必要的响应式

```ts
// 不需要响应式的数据
const CONFIG = {
  API_URL: 'https://api.example.com',
  TIMEOUT: 5000
}

// 需要响应式的数据
const count = ref(0)
```

### 使用 shallowRef 优化大对象

```ts
import { shallowRef } from 'vue'

// 大对象不需要深度响应式
const largeData = shallowRef({ /* ... */ })
```

### 组件懒加载

```vue
<script setup>
import { defineAsyncComponent } from 'vue'

const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>
```

### v-for 使用 key

```vue
<template>
  <div
    v-for="item in list"
    :key="item.id"
  >
    {{ item.name }}
  </div>
</template>
```
