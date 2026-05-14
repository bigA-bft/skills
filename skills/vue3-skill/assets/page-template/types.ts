/**
 * 页面类型定义
 */

/** 页面查询参数 */
export interface PageQuery {
  page?: number
  pageSize?: number
  keyword?: string
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

/** 分页响应 */
export interface PaginatedResponse<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

/** 页面状态 */
export type PageStatus = 'idle' | 'loading' | 'success' | 'error'

/** 表单状态 */
export interface FormState {
  isSubmitting: boolean
  isValid: boolean
  errors: Record<string, string>
}
