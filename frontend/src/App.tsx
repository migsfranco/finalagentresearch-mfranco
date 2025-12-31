import { ChatContainer } from './components/Chat/ChatContainer'
import { Header } from './components/Layout/Header'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <ChatContainer />
      </main>
    </div>
  )
}

export default App
