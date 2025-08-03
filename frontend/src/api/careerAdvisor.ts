import type { PromptsResponse, AdviceRequest, AdviceResponse } from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

// Custom error class for API errors
export class CareerAdvisorApiError extends Error {
  status?: number;
  
  constructor(message: string, status?: number) {
    super(message);
    this.name = 'CareerAdvisorApiError';
    this.status = status;
  }
}

// Generic fetch wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new CareerAdvisorApiError(
        `API request failed: ${response.statusText}`,
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof CareerAdvisorApiError) {
      throw error;
    }
    throw new CareerAdvisorApiError(
      error instanceof Error ? error.message : 'Unknown API error'
    );
  }
}

// API Functions
export const careerAdvisorApi = {
  // Fetch all available prompts
  async getPrompts(): Promise<PromptsResponse> {
    return apiRequest<PromptsResponse>('/prompts/');
  },

  // Submit a question for career advice
  async getAdvice(request: AdviceRequest): Promise<AdviceResponse> {
    return apiRequest<AdviceResponse>('/advice/', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },
};

export default careerAdvisorApi;
