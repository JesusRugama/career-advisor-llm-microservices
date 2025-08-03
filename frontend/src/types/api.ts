// API Response Types
export interface Prompt {
  id: number;
  title: string;
  prompt: string;
}

export interface PromptsResponse {
  success: boolean;
  prompts: Prompt[];
}

export interface AdviceRequest {
  question: string;
}

export interface AdviceResponse {
  id: string;
  choices: {
    finish_reason: string;
    index: number;
    logprobs: null | any;
    message: {
      content: string;
      role?: string;
    };
  }[];
}

// Chat Message Type
export interface ChatMessage {
  id: string;
  question: string;
  response: string;
  timestamp: Date;
}

// API Error Type
export interface ApiError {
  message: string;
  status?: number;
}
