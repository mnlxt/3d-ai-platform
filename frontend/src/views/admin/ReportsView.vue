<template>
  <div class="reports-view">
    <div class="page-header">
      <h1>举报管理</h1>
      <el-radio-group v-model="filterStatus" @change="fetchReports">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="pending">待处理</el-radio-button>
        <el-radio-button label="reviewed">已审核</el-radio-button>
        <el-radio-button label="dismissed">已驳回</el-radio-button>
      </el-radio-group>
    </div>

    <el-card>
      <el-table :data="reports" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="举报作品" min-width="200">
          <template #default="{ row }">
            <div class="project-info">
              <div class="project-title">{{ row.project?.title || '未知作品' }}</div>
              <div class="project-id">ID: {{ row.project_id }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="举报人" width="150">
          <template #default="{ row }">
            {{ row.reporter?.username || '未知用户' }}
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="举报原因" min-width="150" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="action_taken" label="处理结果" width="120">
          <template #default="{ row }">
            <el-tag :type="getActionType(row.action_taken)">
              {{ getActionName(row.action_taken) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="举报时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              size="small"
              type="primary"
              @click="showDetailDialog(row)"
            >
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchReports"
        />
      </div>
    </el-card>

    <!-- 举报详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="举报详情"
      width="600px"
    >
      <div v-if="currentReport" class="report-detail">
        <div class="detail-item">
          <span class="label">举报作品：</span>
          <span>{{ currentReport.project?.title || '未知作品' }} (ID: {{ currentReport.project_id }})</span>
        </div>
        <div class="detail-item">
          <span class="label">作品作者：</span>
          <span>{{ currentReport.project?.owner?.username || '未知' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">举报人：</span>
          <span>{{ currentReport.reporter?.username || '未知用户' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">举报原因：</span>
          <span>{{ currentReport.reason }}</span>
        </div>
        <div class="detail-item">
          <span class="label">详细描述：</span>
          <p class="description">{{ currentReport.description || '无详细描述' }}</p>
        </div>
        <div class="detail-item">
          <span class="label">举报时间：</span>
          <span>{{ formatDate(currentReport.created_at) }}</span>
        </div>
        
        <el-divider />
        
        <h3>处理操作</h3>
        <el-form :model="handleForm" label-width="100px">
          <el-form-item label="处理状态">
            <el-select v-model="handleForm.status" style="width: 100%">
              <el-option label="已审核" value="reviewed" />
              <el-option label="已驳回" value="dismissed" />
            </el-select>
          </el-form-item>
          <el-form-item label="处理措施">
            <el-select v-model="handleForm.action_taken" style="width: 100%">
              <el-option label="无操作" value="none" />
              <el-option label="警告用户" value="warning" />
              <el-option label="删除作品" value="removed" />
              <el-option label="封禁用户" value="banned" />
            </el-select>
          </el-form-item>
          <el-form-item label="管理员备注">
            <el-input
              v-model="handleForm.admin_notes"
              type="textarea"
              :rows="3"
              placeholder="请输入处理备注..."
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleReport">提交处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { reportApi } from '@/api/appeal'
import type { ContentReport } from '@/types/appeal'

const reports = ref<ContentReport[]>([])
const loading = ref(false)
const submitting = ref(false)
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailDialogVisible = ref(false)
const currentReport = ref<ContentReport | null>(null)
const handleForm = ref({
  status: '',
  action_taken: '',
  admin_notes: ''
})

onMounted(() => {
  fetchReports()
})

async function fetchReports() {
  loading.value = true
  try {
    const data = await reportApi.getAllReports(
      (currentPage.value - 1) * pageSize.value,
      pageSize.value,
      filterStatus.value || undefined
    )
    reports.value = data
    total.value = data.length
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '获取举报列表失败')
  } finally {
    loading.value = false
  }
}

function showDetailDialog(report: ContentReport) {
  currentReport.value = report
  handleForm.value.status = report.status
  handleForm.value.action_taken = report.action_taken
  handleForm.value.admin_notes = report.admin_notes || ''
  detailDialogVisible.value = true
}

async function handleReport() {
  if (!currentReport.value) return
  
  submitting.value = true
  try {
    await reportApi.updateReport(currentReport.value.id, {
      status: handleForm.value.status as any,
      action_taken: handleForm.value.action_taken as any,
      admin_notes: handleForm.value.admin_notes,
    })
    ElMessage.success('处理成功')
    detailDialogVisible.value = false
    fetchReports()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '处理失败')
  } finally {
    submitting.value = false
  }
}

function getStatusName(status: string) {
  const statusMap: Record<string, string> = {
    pending: '待处理',
    reviewed: '已审核',
    dismissed: '已驳回'
  }
  return statusMap[status] || status
}

function getStatusType(status: string) {
  const typeMap: Record<string, string> = {
    pending: 'danger',
    reviewed: 'success',
    dismissed: 'info'
  }
  return typeMap[status] || 'info'
}

function getActionName(action: string) {
  const actionMap: Record<string, string> = {
    none: '无操作',
    warning: '警告用户',
    removed: '删除作品',
    banned: '封禁用户'
  }
  return actionMap[action] || action
}

function getActionType(action: string) {
  const typeMap: Record<string, string> = {
    none: 'info',
    warning: 'warning',
    removed: 'danger',
    banned: 'danger'
  }
  return typeMap[action] || 'info'
}

function formatDate(date: string) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<style scoped>
.reports-view {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.project-info {
  .project-title {
    font-weight: 500;
    color: #303133;
    margin-bottom: 4px;
  }
  
  .project-id {
    font-size: 12px;
    color: #909399;
  }
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.report-detail {
  .detail-item {
    margin-bottom: 16px;
    
    .label {
      font-weight: bold;
      color: #606266;
    }
    
    .description {
      margin: 8px 0 0 0;
      padding: 12px;
      background-color: #f5f7fa;
      border-radius: 4px;
      color: #606266;
      line-height: 1.6;
    }
  }
}
</style>
