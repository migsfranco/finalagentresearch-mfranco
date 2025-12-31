/**
 * Tool-related type definitions
 */

export interface ToolInfo {
  name: string
  description: string
  requiresApiKey: boolean
  isAvailable: boolean
}

export interface ToolsResponse {
  tools: ToolInfo[]
  total: number
}
