<template>
  <div class="appeals-view">
    <div class="page-header">
      <h1>申诉管理</h1>
      <el-radio-group v-model="filterStatus" @change="fetchAppeals">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="pending">待处理</el-radio-button>
        <el-radio-button label="processing">处理中</el-radio-button>
        <el-radio-button label="resolved">已解决</el-radio-button>
        <el-radio-button label="rejected">已拒绝</el-radio-button>
      </el-radio-group>
    </div>

    <el-card>
      <el-table :data="appeals" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeType(row.type)">
              {{ getTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申诉人" width="150">
          <template #default="{ row }">
            {{ row.user?.username || '未知用户' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180">
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
          @current-change="fetchAppeals"
        />
      </div>
    </el-card>

    <!-- 申诉详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="申诉详情"
      width="600px"
    >
      <div v-if="currentAppeal" class="appeal-detail">
        <div class="detail-item">
          <span class="label">标题：</span>
          <span>{{ currentAppeal.title }}</span>
        </div>
        <div class="detail-item">
          <span class="label">类型：</span>
          <el-tag :type="getTypeType(currentAppeal.type)">
            {{ getTypeName(currentAppeal.type) }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">申诉人：</span>
          <span>{{ currentAppeal.user?.username }} ({{ currentAppeal.user?.email }})</span>
        </div>
        <div class="detail-item">
          <span class="label">描述：</span>
          <p class="description">{{ currentAppeal.description }}</p>
        </div>
        
        <el-divider />
        
        <el-form :model="handleForm" label-width="100px">
          <el-form-item label="处理状态">
            <el-select v-model="handleForm.status" style="width: 100%">
              <el-option label="处理中" value="processing" />
              <el-option label="已解决" value="resolved" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </el-form-item>
          <el-form-item label="回复内容">
            <el-input
              v-model="handleForm.admin_response"
              type="textarea"
              :rows="4"
              placeholder="请输入回复内容..."
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleAppeal">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { appealApi } from '@/api/appeal'
import type { Appeal } from '@/types/appeal'

const appeals = ref<Appeal[]>([])
const loading = ref(false)
const submitting = ref(false)
const filterStatus = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailDialogVisible = ref(false)
const currentAppeal = ref<Appeal | null>(null)
const handleForm = ref({
  status: '',
  admin_response: ''
})

onMounted(() => {
  fetchAppeals()
})

async function fetchAppeals() {
  loading.value = true
  try {
    const data = await appealApi.getAllAppeals(
      (currentPage.value - 1) * pageSize.value,
      pageSize.value,
      filterStatus.value || undefined
    )
    appeals.value = data
    total.value = data.length
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '获取申诉列表失败')
  } finally {
    loading.value = false
  }
}

function showDetailDialog(appeal: Appeal) {
  currentAppeal.value = appeal
  handleForm.value.status = appeal.status
  handleForm.value.admin_response = appeal.admin_response || ''
  detailDialogVisible.value = true
}

async function handleAppeal() {
  if (!currentAppeal.value) return
  
  submitting.value = true
  try {
    await appealApi.updateAppeal(currentAppeal.value.id, {
      status: handleForm.value.status as any,
      admin_response: handleForm.value.admin_response,
    })
    ElMessage.success('处理成功')
    detailDialogVisible.value = false
    fetchAppeals()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '处理失败')
  } finally {
    submitting.value = false
  }
}

function getTypeName(type: string) {
  const typeMap: Record<string, string> = {
    account: '账号问题',
    content: '内容问题',
    other: '其他'
  }
  return typeMap[type] || type
}

function getTypeType(type: string) {
  const typeMap: Record<string, string> = {
    account: 'danger',
    content: 'warning',
    other: 'info'
  }
  return typeMap[type] || 'info'
}

function getStatusName(status: string) {
  const statusMap: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决',
    rejected: '已拒绝'
  }
  return statusMap[status] || status
}

function getStatusType(status: string) {
  const typeMap: Record<string, string> = {
    pending: 'danger',
    processing: 'warning',
    resolved: 'success',
    rejected: 'info'
  }
  return typeMap[status] || 'info'
}

function formatDate(date: string) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<style scoped>
.appeals-view {
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

.appeal-detail {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
