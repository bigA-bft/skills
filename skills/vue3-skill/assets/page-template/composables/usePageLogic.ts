import { ref } from 'vue'

/**
 * 页面逻辑组合式函数
 * @returns 页面状态和逻辑方法
 */
export function usePageLogic() {
  // 加载状态
  const isLoading = ref(false)

  // 错误信息
  const error = ref<string | null>(null)

  // 其他页面级状态
  const isDirty = ref(false)  // 是否有未保存的修改

  /**
   * 设置页面修改状态
   */
  const setDirty = (value: boolean) => {
    isDirty.value = value
  }

  /**
   * 清除错误
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * 检查是否可以离开页面（用于未保存提示）
   */
  const canLeave = (): boolean => {
    if (isDirty.value) {
      return confirm('有未保存的修改，确定要离开吗？')
    }
    return true
  }

  return {
    isLoading,
    error,
    isDirty,
    setDirty,
    clearError,
    canLeave
  }
}
