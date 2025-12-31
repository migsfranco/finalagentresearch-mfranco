/**
 * Main chat container component
 */

import { useChatStore } from '../../stores/chatStore'
import { MessageList } from './MessageList'
import { ChatInput } from './ChatInput'

export function ChatContainer() {
  const { messages, isLoading, error, sendMessage, clearMessages, clearError } =
    useChatStore()

  const handleSend = async (content: string) => {
    await sendMessage(content)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b">
        <h2 className="text-lg font-medium text-gray-800">Chat</h2>
        <button
          onClick={clearMessages}
          className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
        >
          New conversation
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-red-700">{error}</p>
            <button
              onClick={clearError}
              className="text-red-500 hover:text-red-700"
            >
              &times;
            </button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}
