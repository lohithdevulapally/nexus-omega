import axios from 'axios';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const DEFAULT_ORG_ID = process.env.NEXT_PUBLIC_DEFAULT_ORG_ID || '2d48f08c-0b35-4aea-8941-86e4f855f738';
export const DEFAULT_ORG_NAME = process.env.NEXT_PUBLIC_DEFAULT_ORG_NAME || 'NEXUS Demo Corporation';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = 'An unexpected error occurred';
    const responseData = error.response?.data;
    const statusCode = error.response?.status;
    const requestId = responseData?.request_id;

    if (responseData?.detail) {
      const detail = responseData.detail;
      if (typeof detail === 'string') {
        message = detail;
      } else if (Array.isArray(detail)) {
        // FastAPI validation errors: [{loc: [...], msg: "...", type: "..."}]
        message = detail
          .map((item: any) => {
            const field = Array.isArray(item.loc)
              ? item.loc.filter((part: any) => part !== 'body').join('.') || 'param'
              : 'field';
            return `${field}: ${item.msg || JSON.stringify(item)}`;
          })
          .join('; ');
      } else if (typeof detail === 'object') {
        message = detail.message || detail.error || JSON.stringify(detail);
      }
    } else if (responseData?.message) {
      message = typeof responseData.message === 'string'
        ? responseData.message
        : JSON.stringify(responseData.message);
    } else if (error.message) {
      message = error.message;
    }

    if (statusCode && !message.includes(String(statusCode))) {
      message = `[HTTP ${statusCode}] ${message}`;
    }
    if (requestId) {
      message += ` (Request ID: ${requestId})`;
    }

    const err = new Error(message);
    (err as any).status = statusCode;
    (err as any).requestId = requestId;
    (err as any).data = responseData;
    return Promise.reject(err);
  }
);
