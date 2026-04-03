import type { Project } from './project'

export interface User {
  id: number
  username: string
  email: string
  phone?: string
  avatar_url?: string
  gender?: string
  bio?: string
  role: string
  is_active: boolean
  is_verified: boolean
  preferences?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
  user: User
}

export interface PasswordChange {
  old_password: string
  new_password: string
}

export interface UserPublicResponse {
  user: User
  projects: Project[]
}
