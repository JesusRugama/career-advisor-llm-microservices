import { useState } from "react";
import "./App.css";
import PromptsList from "./components/PromptsList";
import type { ChatMessage } from "./types/api";
import { careerAdvisorApi, CareerAdvisorApiError } from "./api/careerAdvisor";

function App() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePromptClick = (prompt: string) => {
    setCurrentQuestion(prompt);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion.trim() || isLoading) return;

    setIsLoading(true);

    try {
      const data = await careerAdvisorApi.getAdvice({ question: currentQuestion });

      // Add to chat history
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        question: currentQuestion,
        response: data.choices[0].message.content || "Sorry, I could not provide advice at this time.",
        timestamp: new Date(),
      };

      setChatHistory((prev) => [newMessage, ...prev]);
      setCurrentQuestion("");
    } catch (error) {
      console.error("Failed to get advice:", error);
      // Add error message to chat
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        question: currentQuestion,
        response: error instanceof CareerAdvisorApiError
          ? `Error: ${error.message}`
          : "Sorry, there was an error getting your advice. Please try again.",
        timestamp: new Date(),
      };
      setChatHistory((prev) => [errorMessage, ...prev]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Career Advisor</h1>
          <p className="text-gray-600">
            Get personalized career advice powered by AI
          </p>
        </div>
      </header>

      <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-6 flex flex-col gap-6">
        {/* Chat History - Top Section */}
        <div className="flex-1 bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Conversation
          </h2>

          {chatHistory.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <p>
                No conversations yet. Ask a question or select a prompt below to
                get started!
              </p>
            </div>
          ) : (
            <div className="space-y-6 max-h-96 overflow-y-auto">
              {chatHistory.map((message) => (
                <div
                  key={message.id}
                  className="border-b border-gray-100 pb-4 last:border-b-0"
                >
                  <div className="mb-2">
                    <div className="bg-blue-50 rounded-lg p-3 mb-3">
                      <p className="text-sm font-medium text-blue-900 mb-1">
                        Your Question:
                      </p>
                      <p className="text-blue-800">{message.question}</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-3">
                      <p className="text-sm font-medium text-green-900 mb-1">
                        Career Advice:
                      </p>
                      <p className="text-green-800 whitespace-pre-wrap">
                        {message.response}
                      </p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">
                    {message.timestamp.toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Prompts - Middle Section */}
        <PromptsList onPromptClick={handlePromptClick} />

        {/* Question Input - Bottom Section */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="question"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Ask your career question:
              </label>
              <textarea
                id="question"
                value={currentQuestion}
                onChange={(e) => setCurrentQuestion(e.target.value)}
                placeholder="Type your career question here... (e.g., What skills should I focus on developing next?)"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                rows={3}
                disabled={isLoading}
              />
            </div>
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={!currentQuestion.trim() || isLoading}
                className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? "Getting Advice..." : "Get Advice"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
