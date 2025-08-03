import { useState, useEffect } from 'react';
import type { Prompt } from '../types/api';
import { careerAdvisorApi, CareerAdvisorApiError } from '../api/careerAdvisor';

interface PromptsListProps {
  onPromptClick: (prompt: string) => void;
}

export default function PromptsList({ onPromptClick }: PromptsListProps) {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch prompts from API
  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await careerAdvisorApi.getPrompts();
        if (data.success) {
          setPrompts(data.prompts);
        }
      } catch (error) {
        console.error('Failed to fetch prompts:', error);
        const errorMessage = error instanceof CareerAdvisorApiError 
          ? error.message 
          : 'Failed to load prompts';
        setError(errorMessage);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPrompts();
  }, []);

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Quick Start Prompts
      </h2>

      {error ? (
        <div className="text-center text-red-500 py-4">
          <p>Error: {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-2 px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
          >
            Retry
          </button>
        </div>
      ) : isLoading ? (
        <div className="text-center text-gray-500 py-4">
          <p>Loading prompts...</p>
        </div>
      ) : prompts.length === 0 ? (
        <div className="text-center text-gray-500 py-4">
          <p>No prompts available.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {prompts.map((prompt) => (
            <button
              key={prompt.id}
              onClick={() => onPromptClick(prompt.prompt)}
              className="text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
            >
              <h3 className="font-medium text-gray-900 mb-1">{prompt.title}</h3>
              <p className="text-sm text-gray-600 line-clamp-2">
                {prompt.prompt}
              </p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
