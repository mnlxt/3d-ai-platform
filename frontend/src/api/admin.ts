import client from './client'
import type { User } from '@/types/user'
import type { Appeal, ContentReport } from '@/types/appeal'
import type { Project } from '@/types/project'

export interface DashboardStats {
  users: {
    total: number
    new_today: number
    role_distribution: Record<string, number>
  }
  projects: {
    total: number
    new_today: number
    status_distribution: Record<string, number>
  }
  pending_tasks: {
    appeals: number
    reports: number
  }
}

export const adminApi = {
  // 仪表盘统计
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await client.get<DashboardStats>('/admin/dashboard')
    return response.data
  },

  // 用户管理
  async getUsers(params?: {
    skip?: number
    limit?: number
    role?: string
    is_active?: boolean
    search?: string
  }): Promise<User[]> {
    const response = await client.get<User[]>('/users/', { params })
    return response.data
  },

  async updateUserRole(userId: number, role: string): Promise<{ message: string; user: User }> {
    const response = await client.put(`/users/${userId}/role`, null, {
      params: { role }
    })
    return response.data
  },

  async updateUserStatus(userId: number, isActive: boolean): Promise<{ message: string; user: User }> {
    const response = await client.put(`/users/${userId}/status`, null, {
      params: { is_active: isActive }
    })
    return response.data
  },

  async deleteUser(userId: number): Promise<{ message: string }> {
    const response = await client.delete(`/users/${userId}`)
    return response.data
  },

  // 作品管理（管理员）
  async getAllProjects(params?: {
    skip?: number
    limit?: number
    status?: string
    is_public?: boolean
  }): Promise<Project[]> {
    const response = await client.get<Project[]>('/projects/all', { params })
    return response.data
  },

  async toggleProjectPublic(projectId: number, isPublic: boolean): Promise<Project> {
    const response = await client.put<Project>(`/projects/${projectId}/public`, { is_public: isPublic })
    return response.data
  },
}
