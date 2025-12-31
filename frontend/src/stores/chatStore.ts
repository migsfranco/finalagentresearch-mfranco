/**
 * Chat state management using Zustand
 */

import { create } from 'zustand'
import type { Message } from '../types/chat'
import api from '../services/api'

interface ChatState {
  messages: Message[]
  threadId: string
  isLoading: boolean
  error: string | null

  // Actions
  sendMessage: (content: string) => Promise<void>
  clearMessages: () => void
  setThreadId: (id: string) => void
  clearError: () => void
}

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  threadId: generateId(),
  isLoading: false,
  error: null,

  sendMessage: async (content: string) => {
    const { threadId, messages } = get()

    // Add user message immediately
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date(),
    }

    set({
      messages: [...messages, userMessage],
      isLoading: true,
      error: null,
    })

    try {
      const response = await api.chat(content, threadId)

      if (response.error) {
        set({ error: response.error, isLoading: false })
        return
      }

      if (response.data) {
        const assistantMessage: Message = {
          id: generateId(),
          role: 'assistant',
          content: response.data.final_response,
          timestamp: new Date(),
        }

        set((state) => ({
          messages: [...state.messages, assistantMessage],
          isLoading: false,
        }))
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to send message',
        isLoading: false,
      })
    }
  },

  clearMessages: () => {
    set({
      messages: [],
      threadId: generateId(),
      error: null,
    })
  },

  setThreadId: (id: string) => {
    set({ threadId: id })
  },

  clearError: () => {
    set({ error: null })
  },
}))
