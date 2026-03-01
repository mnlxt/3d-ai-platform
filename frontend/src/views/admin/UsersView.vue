<template>
  <div class="users-view">
    <div class="page-header">
      <h1>用户管理</h1>
      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名或邮箱"
          style="width: 200px"
          clearable
          @keyup.enter="fetchUsers"
        />
        <el-select v-model="filterRole" placeholder="角色" clearable @change="fetchUsers">
          <el-option label="管理员" value="admin" />
          <el-option label="创作者" value="creator" />
          <el-option label="查看者" value="viewer" />
        </el-select>
        <el-select v-model="filterStatus" placeholder="状态" clearable @change="fetchUsers">
          <el-option label="正常" :value="true" />
          <el-option label="禁用" :value="false" />
        </el-select>
        <el-button type="primary" @click="fetchUsers">搜索</el-button>
      </div>
    </div>

    <el-card>
      <el-table :data="users" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户" min-width="200">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="40" :src="row.avatar_url || '/default-avatar.png'" />
              <div class="user-details">
                <div class="username">{{ row.username }}</div>
                <div class="email">{{ row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleName(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              size="small"
              @click="showEditDialog(row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              :type="row.is_active ? 'danger' : 'success'"
              @click="toggleUserStatus(row)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-popconfirm
              title="确定要删除该用户吗？此操作不可恢复！"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="deleteUser(row.id)"
            >
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchUsers"
        />
      </div>
    </el-card>

    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑用户"
      width="500px"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" disabled />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="创作者" value="creator" />
            <el-option label="查看者" value="viewer" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="editForm.is_active"
            active-text="正常"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="updateUser">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/admin'
import type { User } from '@/types/user'

const users = ref<User[]>([])
const loading = ref(false)
const submitting = ref(false)
const searchQuery = ref('')
const filterRole = ref('')
const filterStatus = ref<boolean | ''>('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const editDialogVisible = ref(false)
const editForm = ref({
  id: 0,
  username: '',
  email: '',
  role: '',
  is_active: true
})

onMounted(() => {
  fetchUsers()
})

async function fetchUsers() {
  loading.value = true
  try {
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    }
    if (searchQuery.value) params.search = searchQuery.value
    if (filterRole.value) params.role = filterRole.value
    if (filterStatus.value !== '') params.is_active = filterStatus.value
    
    const data = await adminApi.getUsers(params)
    users.value = data
    total.value = data.length
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '获取用户列表失败')
  } finally {
    loading.value = false
  }
}

function showEditDialog(user: User) {
  editForm.value = {
    id: user.id!,
    username: user.username,
    email: user.email,
    role: user.role,
    is_active: user.is_active
  }
  editDialogVisible.value = true
}

async function updateUser() {
  submitting.value = true
  try {
    // 更新角色
    if (editForm.value.role) {
      await adminApi.updateUserRole(editForm.value.id, editForm.value.role)
    }
    // 更新状态
    await adminApi.updateUserStatus(editForm.value.id, editForm.value.is_active)
    
    ElMessage.success('用户更新成功')
    editDialogVisible.value = false
    fetchUsers()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '更新失败')
  } finally {
    submitting.value = false
  }
}

async function toggleUserStatus(user: User) {
  try {
    const action = user.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.username}" 吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await adminApi.updateUserStatus(user.id!, !user.is_active)
    ElMessage.success(`用户已${action}`)
    fetchUsers()
  } catch (err: any) {
    if (err !== 'cancel') {
      ElMessage.error(err.response?.data?.detail || '操作失败')
    }
  }
}

async function deleteUser(userId: number) {
  try {
    await adminApi.deleteUser(userId)
    ElMessage.success('用户已删除')
    fetchUsers()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '删除失败')
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

function formatDate(date: string) {
  return new Date(date).toLocaleString('zh-CN')
}
</script>

<style scoped>
.users-view {
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

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 500;
  color: #303133;
}

.email {
  font-size: 12px;
  color: #909399;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
