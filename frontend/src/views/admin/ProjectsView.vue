<template>
  <div class="projects-view">
    <div class="page-header">
      <h1>作品审核</h1>
      <div class="filter-bar">
        <el-select v-model="filterStatus" placeholder="状态" clearable @change="fetchProjects">
          <el-option label="草稿" value="draft" />
          <el-option label="处理中" value="processing" />
          <el-option label="已完成" value="completed" />
          <el-option label="已归档" value="archived" />
        </el-select>
        <el-select v-model="filterPublic" placeholder="可见性" clearable @change="fetchProjects">
          <el-option label="公开" :value="true" />
          <el-option label="私密" :value="false" />
        </el-select>
        <el-button type="primary" @click="fetchProjects">刷新</el-button>
      </div>
    </div>

    <el-card>
      <el-table :data="projects" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="作品信息" min-width="250">
          <template #default="{ row }">
            <div class="project-info">
              <div class="project-title">{{ row.title }}</div>
              <div class="project-desc">{{ row.description || '暂无描述' }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="作者" width="150">
          <template #default="{ row }">
            {{ row.owner?.username || '未知用户' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_public" label="可见性" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_public ? 'success' : 'info'">
              {{ row.is_public ? '公开' : '私密' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              size="small"
              @click="showDetailDialog(row)"
            >
              详情
            </el-button>
            <el-button
              size="small"
              :type="row.is_public ? 'warning' : 'success'"
              @click="togglePublic(row)"
            >
              {{ row.is_public ? '设为私密' : '设为公开' }}
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
          @current-change="fetchProjects"
        />
      </div>
    </el-card>

    <!-- 作品详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="作品详情"
      width="700px"
    >
      <div v-if="currentProject" class="project-detail">
        <div class="detail-section">
          <h3>基本信息</h3>
          <div class="detail-item">
            <span class="label">标题：</span>
            <span>{{ currentProject.title }}</span>
          </div>
          <div class="detail-item">
            <span class="label">作者：</span>
            <span>{{ currentProject.owner?.username }} ({{ currentProject.owner?.email }})</span>
          </div>
          <div class="detail-item">
            <span class="label">状态：</span>
            <el-tag :type="getStatusType(currentProject.status)">
              {{ getStatusName(currentProject.status) }}
            </el-tag>
          </div>
          <div class="detail-item">
            <span class="label">可见性：</span>
            <el-tag :type="currentProject.is_public ? 'success' : 'info'">
              {{ currentProject.is_public ? '公开' : '私密' }}
            </el-tag>
          </div>
          <div class="detail-item">
            <span class="label">创建时间：</span>
            <span>{{ formatDate(currentProject.created_at) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">更新时间：</span>
            <span>{{ formatDate(currentProject.updated_at) }}</span>
          </div>
        </div>

        <div class="detail-section">
          <h3>描述</h3>
          <p class="description">{{ currentProject.description || '暂无描述' }}</p>
        </div>

        <div class="detail-section">
          <h3>3D模型数据</h3>
          <div class="detail-item">
            <span class="label">模型路径：</span>
            <code>{{ currentProject.model_data?.model_path || 'N/A' }}</code>
          </div>
          <div class="detail-item">
            <span class="label">纹理路径：</span>
            <code>{{ currentProject.model_data?.texture_path || 'N/A' }}</code>
          </div>
          <div class="detail-item">
            <span class="label">材质路径：</span>
            <code>{{ currentProject.model_data?.material_path || 'N/A' }}</code>
          </div>
          <div class="detail-item">
            <span class="label">预览图：</span>
            <code>{{ currentProject.model_data?.preview_image || 'N/A' }}</code>
          </div>
        </div>

        <div class="detail-section">
          <h3>操作</h3>
          <div class="action-buttons">
            <el-button
              :type="currentProject.is_public ? 'warning' : 'success'"
              @click="togglePublic(currentProject); detailDialogVisible = false"
            >
              {{ currentProject.is_public ? '设为私密' : '设为公开' }}
            </el-button>
            <el-button type="primary" @click="viewProject(currentProject.id)">
              查看作品
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminApi } from '@/api/admin'
import type { Project } from '@/types/project'

const router = useRouter()

const projects = ref<Project[]>([])
const loading = ref(false)
const filterStatus = ref('')
const filterPublic = ref<boolean | ''>('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailDialogVisible = ref(false)
const currentProject = ref<Project | null>(null)

onMounted(() => {
  fetchProjects()
})

async function fetchProjects() {
  loading.value = true
  try {
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    }
    if (filterStatus.value) params.status = filterStatus.value
    if (filterPublic.value !== '') params.is_public = filterPublic.value
    
    const data = await adminApi.getAllProjects(params)
    projects.value = data
    total.value = data.length
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '获取作品列表失败')
  } finally {
    loading.value = false
  }
}

function showDetailDialog(project: Project) {
  currentProject.value = project
  detailDialogVisible.value = true
}

async function togglePublic(project: Project) {
  try {
    await adminApi.toggleProjectPublic(project.id!, !project.is_public)
    ElMessage.success(project.is_public ? '作品已设为私密' : '作品已设为公开')
    fetchProjects()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

function viewProject(projectId: number) {
  router.push(`/library/project/${projectId}`)
}

function getStatusName(status: string) {
  const statusMap: Record<string, string> = {
    draft: '草稿',
    processing: '处理中',
    completed: '已完成',
    archived: '已归档'
  }
  return statusMap[status] || status
}

function getStatusType(status: string) {
  const typeMap: Record<string, string> = {
    draft: 'info',
    processing: 'warning',
    completed: 'success',
    archived: ''
  }
  return typeMap[status] || ''
}

function formatDate(date: string) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<style scoped>
.projects-view {
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

.filter-bar {
  display: flex;
  gap: 10px;
}

.project-info {
  .project-title {
    font-weight: 500;
    color: #303133;
    margin-bottom: 4px;
  }
  
  .project-desc {
    font-size: 12px;
    color: #909399;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
  }
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.project-detail {
  .detail-section {
    margin-bottom: 24px;
    
    h3 {
      margin: 0 0 12px 0;
      font-size: 16px;
      color: #303133;
      border-bottom: 1px solid #EBEEF5;
      padding-bottom: 8px;
    }
    
    .detail-item {
      margin-bottom: 12px;
      
      .label {
        font-weight: 500;
        color: #606266;
        display: inline-block;
        width: 100px;
      }
      
      code {
        background-color: #f5f7fa;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        color: #606266;
      }
    }
    
    .description {
      margin: 0;
      padding: 12px;
      background-color: #f5f7fa;
      border-radius: 4px;
      color: #606266;
      line-height: 1.6;
    }
    
    .action-buttons {
      display: flex;
      gap: 12px;
    }
  }
}
</style>
