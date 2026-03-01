<template>
  <div class="profile-setup-container">
    <div class="setup-card">
      <div class="setup-header">
        <h1>完善个人信息</h1>
        <p class="subtitle">让我们更好地了解您（可选）</p>
      </div>

      <el-form
        ref="setupFormRef"
        :model="setupForm"
        :rules="setupRules"
        label-width="100px"
        class="setup-form"
      >
        <el-form-item label="头像">
          <div class="avatar-section">
            <el-avatar
              :size="100"
              :src="setupForm.avatar_url || undefined"
              icon="User"
            />
            <el-input
              v-model="setupForm.avatar_url"
              placeholder="头像URL"
              style="margin-top: 12px"
            />
          </div>
        </el-form-item>

        <el-form-item label="性别">
          <el-select
            v-model="setupForm.gender"
            placeholder="请选择性别"
            style="width: 100%"
          >
            <el-option label="👨 男" value="male" />
            <el-option label="👩 女" value="female" />
            <el-option label="🤫 保密" value="secret" />
          </el-select>
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="setupForm.phone"
            placeholder="手机号"
          />
        </el-form-item>

        <el-form-item label="个人签名">
          <el-input
            v-model="setupForm.bio"
            type="textarea"
            :rows="4"
            placeholder="介绍一下自己吧..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <div class="setup-actions">
          <el-button size="large" @click="skipSetup">
            跳过
          </el-button>
          <el-button
            type="primary"
            size="large"
            :loading="saving"
            @click="saveProfile"
          >
            保存并继续
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const setupFormRef = ref<FormInstance>()
const saving = ref(false)

const setupForm = reactive({
  avatar_url: '',
  gender: 'secret' as 'male' | 'female' | 'secret',
  phone: '',
  bio: '',
})

const setupRules: FormRules = {
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号',
      trigger: 'blur',
    },
  ],
}

async function skipSetup() {
  router.push('/')
}

async function saveProfile() {
  if (!setupFormRef.value) return

  await setupFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      const success = await authStore.updateProfile({
        avatar_url: setupForm.avatar_url || undefined,
        gender: setupForm.gender,
        phone: setupForm.phone || undefined,
        bio: setupForm.bio || undefined,
      })
      saving.value = false

      if (success) {
        ElMessage.success('个人信息保存成功')
        router.push('/')
      } else {
        ElMessage.error(authStore.error || '保存失败')
      }
    }
  })
}
</script>

<style scoped>
.profile-setup-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.setup-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.setup-header {
  text-align: center;
  margin-bottom: 32px;
}

.setup-header h1 {
  font-size: 28px;
  color: #333;
  margin: 0 0 8px 0;
}

.setup-header .subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

.setup-form {
  margin-top: 24px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.setup-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
}

.setup-actions .el-button {
  min-width: 140px;
}
</style>
