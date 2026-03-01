import client from './client'
import type { Appeal, AppealCreate, AppealUpdate, ContentReport, ContentReportCreate, ContentReportUpdate } from '@/types/appeal'

export const appealApi = {
  // 用户提交申诉
  async createAppeal(data: AppealCreate): Promise<Appeal> {
    const response = await client.post<Appeal>('/appeals/', data)
    return response.data
  },

  // 获取我的申诉列表
  async getMyAppeals(): Promise<Appeal[]> {
    const response = await client.get<Appeal[]>('/appeals/my')
    return response.data
  },

  // 获取申诉详情
  async getAppeal(id: number): Promise<Appeal> {
    const response = await client.get<Appeal>(`/appeals/${id}`)
    return response.data
  },

  // 管理员获取所有申诉列表
  async getAllAppeals(skip: number = 0, limit: number = 100, status?: string): Promise<Appeal[]> {
    const params: Record<string, any> = { skip, limit }
    if (status) params.status = status
    const response = await client.get<Appeal[]>('/appeals/', { params })
    return response.data
  },

  // 管理员处理申诉
  async updateAppeal(id: number, data: AppealUpdate): Promise<Appeal> {
    const response = await client.put<Appeal>(`/appeals/${id}`, data)
    return response.data
  },
}

export const reportApi = {
  // 提交内容举报
  async createReport(data: ContentReportCreate): Promise<ContentReport> {
    const response = await client.post<ContentReport>('/moderation/reports', data)
    return response.data
  },

  // 获取所有举报列表（管理员）
  async getAllReports(skip: number = 0, limit: number = 100, status?: string): Promise<ContentReport[]> {
    const params: Record<string, any> = { skip, limit }
    if (status) params.status = status
    const response = await client.get<ContentReport[]>('/moderation/reports', { params })
    return response.data
  },

  // 处理举报（管理员）
  async updateReport(id: number, data: ContentReportUpdate): Promise<ContentReport> {
    const response = await client.put<ContentReport>(`/moderation/reports/${id}`, data)
    return response.data
  },
}
