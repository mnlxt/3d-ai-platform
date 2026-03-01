export interface Appeal {
  id: number
  user_id: number
  type: 'account' | 'content' | 'other'
  title: string
  description: string
  status: 'pending' | 'processing' | 'resolved' | 'rejected'
  admin_response?: string
  resolved_by?: number
  resolved_at?: string
  attachments?: string[]
  created_at: string
  updated_at: string
  user?: {
    id: number
    username: string
    email: string
  }
  resolver?: {
    id: number
    username: string
  }
}

export interface AppealCreate {
  type: 'account' | 'content' | 'other'
  title: string
  description: string
  attachments?: string[]
}

export interface AppealUpdate {
  status?: 'pending' | 'processing' | 'resolved' | 'rejected'
  admin_response?: string
}

export interface ContentReport {
  id: number
  reporter_id: number
  project_id: number
  reason: string
  description?: string
  status: 'pending' | 'reviewed' | 'dismissed'
  admin_notes?: string
  action_taken: 'none' | 'warning' | 'removed' | 'banned'
  reviewed_by?: number
  reviewed_at?: string
  created_at: string
  updated_at: string
  reporter?: {
    id: number
    username: string
  }
  project?: {
    id: number
    title: string
  }
  reviewer?: {
    id: number
    username: string
  }
}

export interface ContentReportCreate {
  project_id: number
  reason: string
  description?: string
}

export interface ContentReportUpdate {
  status?: 'pending' | 'reviewed' | 'dismissed'
  admin_notes?: string
  action_taken?: 'none' | 'warning' | 'removed' | 'banned'
}
