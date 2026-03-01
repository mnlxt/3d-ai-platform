<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="220px" class="admin-sidebar">
        <div class="sidebar-header">
          <h2>管理后台</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="admin-menu"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><DataLine /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/appeals">
            <el-icon><Message /></el-icon>
            <span>申诉管理</span>
            <el-badge v-if="pendingAppeals > 0" :value="pendingAppeals" class="menu-badge" />
          </el-menu-item>
          
          <el-menu-item index="/admin/projects">
            <el-icon><Folder /></el-icon>
            <span>作品审核</span>
          </el-menu-item>
          
          <el-menu-item index="/admin/reports">
            <el-icon><Warning /></el-icon>
            <span>举报管理</span>
            <el-badge v-if="pendingReports > 0" :value="pendingReports" class="menu-badge" />
          </el-menu-item>
          
          <el-divider />
          
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>返回前台</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="admin-header">
          <div class="header-left">
            <span class="breadcrumb">管理员控制台</span>
          </div>
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-avatar :size="32" :src="authStore.user?.avatar_url" />
                <span class="username">{{ authStore.user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  DataLine,
  User,
  Message,
  Folder,
  Warning,
  HomeFilled,
  ArrowDown
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)
const pendingAppeals = ref(0)
const pendingReports = ref(0)

onMounted(() => {
  fetchPendingCounts()
})

async function fetchPendingCounts() {
  // TODO: 从API获取待处理数量
  pendingAppeals.value = 0
  pendingReports.value = 0
}

function handleCommand(command: string) {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    handleLogout()
  }
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await authStore.logout()
    ElMessage.success('已退出登录')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-sidebar {
  background-color: #304156;
  min-height: 100vh;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #1f2d3d;
}

.sidebar-header h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.admin-menu {
  border-right: none;
}

.menu-badge {
  margin-left: 8px;
}

.admin-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.breadcrumb {
  font-size: 14px;
  color: #606266;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #606266;
}

.admin-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
