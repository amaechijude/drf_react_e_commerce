export interface LoginUserRequest {
  email: string;
  password: string;
}

export interface LoginUserResponse {
  readonly access_token: string;
  readonly refresh_token: string;
}
