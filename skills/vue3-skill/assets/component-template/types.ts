/**
 * 组件类型定义
 */

/** 组件状态 */
export type ComponentStatus = 'idle' | 'loading' | 'success' | 'error'

/** 组件数据项 */
export interface ComponentItem {
  id: string | number
  name: string
  value?: unknown
}

/** 组件配置 */
export interface ComponentConfig {
  enabled: boolean
  maxCount: number
  items: ComponentItem[]
}
