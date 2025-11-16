declare module '@/api' {
  interface ApiResponse {
    data: {
      session: {
        access_token: string;
      };
    };
  }

  export const api: {
    post(url: string, data: any): Promise<ApiResponse>;
  };
}