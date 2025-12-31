/**
 * API client for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

interface ApiResponse<T> {
  data: T | null
  error: string | null
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return {
        data: null,
        error: errorData.detail || `HTTP error: ${response.status}`,
      }
    }

    const data = await response.json()
    return { data, error: null }
  } catch (error) {
    return {
      data: null,
      error: error instanceof Error ? error.message : 'Unknown error',
    }
  }
}

export const api = {
  // Health endpoints
  health: () => fetchApi<{ status: string }>('/health'),
  ready: () => fetchApi<{ status: string }>('/ready'),

  // Chat endpoints
  chat: (message: string, threadId: string) =>
    fetchApi<{
      thread_id: string
      messages: Array<{ role: string; content: string }>
      final_response: string
    }>('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, thread_id: threadId }),
    }),

  deleteThread: (threadId: string) =>
    fetchApi<{ status: string }>(`/chat/${threadId}`, {
      method: 'DELETE',
    }),

  // Tools endpoints
  listTools: () =>
    fetchApi<{
      tools: Array<{
        name: string
        description: string
        requires_api_key: boolean
        is_available: boolean
      }>
      total: number
    }>('/tools'),

  getTool: (toolName: string) =>
    fetchApi<{
      name: string
      description: string
      requires_api_key: boolean
      is_available: boolean
    }>(`/tools/${toolName}`),
}

export default api
