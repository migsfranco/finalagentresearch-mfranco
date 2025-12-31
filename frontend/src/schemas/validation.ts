/**
 * Zod validation schemas
 */

import { z } from 'zod'

export const messageSchema = z.object({
  id: z.string(),
  role: z.enum(['user', 'assistant', 'system', 'tool']),
  content: z.string(),
  timestamp: z.date(),
})

export const chatRequestSchema = z.object({
  message: z.string().min(1).max(10000),
  threadId: z.string().min(1).max(100),
})

export const chatResponseSchema = z.object({
  threadId: z.string(),
  messages: z.array(messageSchema),
  finalResponse: z.string(),
})

export const toolInfoSchema = z.object({
  name: z.string(),
  description: z.string(),
  requiresApiKey: z.boolean(),
  isAvailable: z.boolean(),
})

export const toolsResponseSchema = z.object({
  tools: z.array(toolInfoSchema),
  total: z.number(),
})

// Type inference from schemas
export type MessageSchema = z.infer<typeof messageSchema>
export type ChatRequestSchema = z.infer<typeof chatRequestSchema>
export type ChatResponseSchema = z.infer<typeof chatResponseSchema>
export type ToolInfoSchema = z.infer<typeof toolInfoSchema>
export type ToolsResponseSchema = z.infer<typeof toolsResponseSchema>
