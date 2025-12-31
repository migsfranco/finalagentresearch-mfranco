/**
 * Chat-related type definitions
 */

export type MessageRole = 'user' | 'assistant' | 'system' | 'tool'

export interface Message {
  id: string
  role: MessageRole
  content: string
  timestamp: Date
  toolCalls?: ToolCall[]
}

export interface ToolCall {
  id: string
  name: string
  input: Record<string, unknown>
  output?: string
}

export interface ChatRequest {
  message: string
  threadId: string
}

export interface ChatResponse {
  threadId: string
  messages: Message[]
  finalResponse: string
}

export interface ConversationThread {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}
