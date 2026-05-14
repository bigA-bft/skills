<script setup lang="ts">
/**
 * {{COMPONENT_DESCRIPTION}}
 */

// 1. 类型导入
import type { PropType } from 'vue'

// 2. 组合式函数/工具导入
import { ref, computed, watch } from 'vue'

// 3. 组件导入
// import ChildComponent from './ChildComponent.vue'

// 4. 类型定义
interface Props {
  /** 标题 */
  title?: string
  /** 是否禁用 */
  disabled?: boolean
}

interface Emits {
  /** 点击事件 */
  click: [event: MouseEvent]
  /** 更新事件 */
  update: [value: string]
}

// 5. Props 定义
const props = withDefaults(defineProps<Props>(), {
  title: '',
  disabled: false
})

// 6. Emits 定义
const emit = defineEmits<Emits>()

// 7. 响应式状态
const internalValue = ref('')
const isActive = ref(false)

// 8. 计算属性
const displayTitle = computed(() => {
  return props.title || '默认标题'
})

// 9. 监听
watch(internalValue, (newVal, oldVal) => {
  emit('update', newVal)
})

// 10. 方法
const handleClick = (event: MouseEvent) => {
  if (props.disabled) return
  isActive.value = !isActive.value
  emit('click', event)
}
</script>

<template>
  <div
    class="component-name"
    :class="{ 'is-active': isActive, 'is-disabled': disabled }"
    @click="handleClick"
  >
    <h3 class="component-name__title">{{ displayTitle }}</h3>
    <div class="component-name__content">
      <slot>默认内容</slot>
    </div>
  </div>
</template>

<style scoped>
.component-name {
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.component-name.is-active {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.component-name.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.component-name__title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 500;
}

.component-name__content {
  font-size: 14px;
  color: #606266;
}
</style>
