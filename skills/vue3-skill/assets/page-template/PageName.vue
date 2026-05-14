<script setup lang="ts">
/**
 * {{PAGE_DESCRIPTION}}
 */

// 1. Vue 核心导入
import { ref, computed, onMounted } from 'vue'

// 2. 路由（如需要）
// import { useRoute, useRouter } from 'vue-router'

// 3. 状态管理（如需要）
// import { useStore } from '@/store'

// 4. 组合式函数
import { usePageLogic } from './composables/usePageLogic'

// 5. 组件导入
// import PageHeader from '@/components/PageHeader.vue'

// 6. 工具函数
// import { formatDate } from '@/utils/date'

// 7. API（如需要）
// import { fetchPageData } from '@/api/pageApi'

// === 类型定义 ===
interface PageData {
  id: number
  title: string
  content: string
  createdAt: string
}

// === 路由 ===
// const route = useRoute()
// const router = useRouter()

// === 组合式函数 ===
const { isLoading, error } = usePageLogic()

// === 响应式状态 ===
const pageData = ref<PageData | null>(null)
const searchQuery = ref('')
const currentPage = ref(1)

// === 计算属性 ===
const isEmpty = computed(() => !pageData.value)

const filteredData = computed(() => {
  if (!searchQuery.value) return pageData.value
  // 过滤逻辑
  return pageData.value
})

// === 方法 ===
const loadData = async () => {
  isLoading.value = true
  error.value = null
  try {
    // const data = await fetchPageData()
    // pageData.value = data
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const handleRefresh = () => {
  loadData()
}

// === 生命周期 ===
onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="page-name">
    <!-- 页面头部 -->
    <header class="page-name__header">
      <h1 class="page-name__title">页面标题</h1>
      <div class="page-name__actions">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索..."
          class="page-name__search"
          @keyup.enter="handleSearch"
        />
        <button class="page-name__refresh" @click="handleRefresh">
          刷新
        </button>
      </div>
    </header>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="page-name__loading">
      加载中...
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="page-name__error">
      {{ error }}
      <button @click="loadData">重试</button>
    </div>

    <!-- 空状态 -->
    <div v-else-if="isEmpty" class="page-name__empty">
      暂无数据
    </div>

    <!-- 主内容 -->
    <main v-else class="page-name__content">
      <slot>
        <!-- 页面内容区域 -->
        <pre>{{ filteredData }}</pre>
      </slot>
    </main>
  </div>
</template>

<style scoped>
.page-name {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-name__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.page-name__title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.page-name__actions {
  display: flex;
  gap: 12px;
}

.page-name__search {
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
}

.page-name__refresh {
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.page-name__refresh:hover {
  background: #40a9ff;
}

.page-name__loading,
.page-name__error,
.page-name__empty {
  padding: 48px;
  text-align: center;
  color: #999;
}

.page-name__error {
  color: #ff4d4f;
}

.page-name__content {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  min-height: 400px;
}
</style>
