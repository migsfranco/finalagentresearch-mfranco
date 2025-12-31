/**
 * Message list component
 */

import type { Message } from '../../types/chat'
import { MessageBubble } from './MessageBubble'

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-500 p-8">
        <svg
          className="w-16 h-16 mb-4 text-gray-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
        <h3 className="text-lg font-medium mb-2">Start a conversation</h3>
        <p className="text-center text-sm max-w-md">
          Ask me to search for scientific papers, find articles on specific topics,
          or correct your APA citations.
        </p>
        <div className="mt-6 grid grid-cols-1 gap-2 text-sm">
          <span className="px-3 py-2 bg-gray-100 rounded-lg">
            "Find 2 papers about AI in healthcare"
          </span>
          <span className="px-3 py-2 bg-gray-100 rounded-lg">
            "What is ArXiv paper 2510.13422 about?"
          </span>
          <span className="px-3 py-2 bg-gray-100 rounded-lg">
            "Correct this citation: (Gomez et al, 2023, pag. 23)"
          </span>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      {isLoading && (
        <div className="flex items-center gap-2 text-gray-500">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
          <span className="text-sm">Searching...</span>
        </div>
      )}
    </div>
  )
}
