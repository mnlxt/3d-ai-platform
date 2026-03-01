<template>
  <div class="dashboard-view">
    <h1>管理员仪表盘</h1>
    <p>欢迎回来，{{ authStore.user?.username }}</p>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon user-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.users?.total || 0 }}</div>
            <div class="stat-label">总用户数</div>
            <div class="stat-sub">今日新增: +{{ stats.users?.new_today || 0 }}</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon project-icon">
            <el-icon><Folder /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.projects?.total || 0 }}</div>
            <div class="stat-label">总作品数</div>
            <div class="stat-sub">今日新增: +{{ stats.projects?.new_today || 0 }}</div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon appeal-icon">
            <el-icon><Message /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.pending_tasks?.appeals || 0 }}</div>
            <div class="stat-label">待处理申诉</div>
            <el-button
              v-if="stats.pending_tasks?.appeals > 0"
              type="primary"
              size="small"
              @click="$router.push('/admin/appeals')"
            >
              去处理
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon report-icon">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.pending_tasks?.reports || 0 }}</div>
            <div class="stat-label">待处理举报</div>
            <el-button
              v-if="stats.pending_tasks?.reports > 0"
              type="primary"
              size="small"
              @click="$router.push('/admin/reports')"
            >
              去处理
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card v-loading="loading">
          <template #header>
            <span>用户角色分布</span>
          </template>
          <div class="chart-placeholder">
            <div v-if="hasRoleDistribution" class="role-stats">
              <div
                v-for="(count, role) in stats.users?.role_distribution"
                :key="role"
                class="role-item"
              >
                <span class="role-name">{{ getRoleName(role) }}:</span>
                <el-tag :type="getRoleType(role)">{{ count }}人</el-tag>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card v-loading="loading">
          <template #header>
            <span>作品状态分布</span>
          </template>
          <div class="chart-placeholder">
            <div v-if="hasStatusDistribution" class="status-stats">
              <div
                v-for="(count, status) in stats.projects?.status_distribution"
                :key="status"
                class="status-item"
              >
                <span class="status-name">{{ getStatusName(status) }}:</span>
                <el-tag :type="getStatusType(status)">{{ count }}个</el-tag>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { adminApi, type DashboardStats } from '@/api/admin'
import { User, Folder, Message, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

const loading = ref(false)
const stats = ref<DashboardStats>({
  users: { total: 0, new_today: 0, role_distribution: {} },
  projects: { total: 0, new_today: 0, status_distribution: {} },
  pending_tasks: { appeals: 0, reports: 0 }
})

const hasRoleDistribution = computed(() => {
  return stats.value.users?.role_distribution &&
    Object.keys(stats.value.users.role_distribution).length > 0
})

const hasStatusDistribution = computed(() => {
  return stats.value.projects?.status_distribution &&
    Object.keys(stats.value.projects.status_distribution).length > 0
})

onMounted(() => {
  fetchStats()
})

async function fetchStats() {
  loading.value = true
  try {
    const data = await adminApi.getDashboardStats()
    stats.value = data
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '获取统计数据失败')
  } finally {
    loading.value = false
  }
}

function getRoleName(role: string) {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    creator: '创作者',
    viewer: '查看者'
  }
  return roleMap[role] || role
}

function getRoleType(role: string) {
  const typeMap: Record<string, string> = {
    admin: 'danger',
    creator: 'warning',
    viewer: 'info'
  }
  return typeMap[role] || 'info'
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
</script>

<style scoped>
.dashboard-view {
  padding: 20px;
}

h1 {
  margin-bottom: 8px;
  font-size: 24px;
  color: #303133;
}

p {
  color: #909399;
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon .el-icon {
  font-size: 32px;
  color: #fff;
}

.user-icon {
  background-color: #409EFF;
}

.project-icon {
  background-color: #67C23A;
}

.appeal-icon {
  background-color: #E6A23C;
}

.report-icon {
  background-color: #F56C6C;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-sub {
  font-size: 12px;
  color: #67C23A;
}

.charts-row {
  margin-top: 20px;
}

.chart-placeholder {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-stats, .status-stats {
  width: 100%;
}

.role-item, .status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #EBEEF5;
}

.role-item:last-child, .status-item:last-child {
  border-bottom: none;
}

.role-name, .status-name {
  color: #606266;
}
</style>
