import * as THREE from 'three'
import TWEEN from '@tweenjs/tween.js'
import type { ModelConfig } from './types'

export class MultiModelManager {
  private scene: THREE.Scene
  private modelsGroup: THREE.Group
  private models: Map<string, THREE.Object3D> = new Map()
  private selectedModel: THREE.Object3D | null = null

  constructor(scene: THREE.Scene) {
    this.scene = scene
    this.modelsGroup = new THREE.Group()
    this.scene.add(this.modelsGroup)
  }

  /**
   * 添加模型到场景
   */
  addModel(model: THREE.Object3D, config: Omit<ModelConfig, 'id'> & { id?: string }): string {
    const modelId = config.id || THREE.MathUtils.generateUUID()
    
    model.position.set(config.position.x, config.position.y, config.position.z)
    model.rotation.set(config.rotation.x, config.rotation.y, config.rotation.z)
    model.scale.setScalar(config.scale)
    model.visible = config.visible ?? true
    
    model.userData = {
      ...config.userData,
      id: modelId,
      name: config.name,
      filePath: config.filePath,
      fileType: config.fileType,
      originalPosition: { ...config.position },
      originalRotation: { ...config.rotation },
      originalScale: config.scale
    }

    this.modelsGroup.add(model)
    this.models.set(modelId, model)
    
    return modelId
  }

  /**
   * 选择模型
   */
  selectModel(modelId: string): ModelConfig | null {
    const model = this.models.get(modelId)
    if (!model) return null

    this.selectedModel = model
    this.highlightSelectedModel(model)
    
    return this.getModelConfig(model)
  }

  /**
   * 高亮选中模型
   */
  private highlightSelectedModel(model: THREE.Object3D): void {
    this.modelsGroup.children.forEach(child => {
      if (child.userData.isHighlighted) {
        child.userData.isHighlighted = false
        if (child instanceof THREE.Mesh && child.userData.originalMaterial) {
          child.material = child.userData.originalMaterial
        }
      }
    })

    model.userData.isHighlighted = true
    
    if (model instanceof THREE.Mesh) {
      model.userData.originalMaterial = model.material.clone()
      const highlightMaterial = new THREE.MeshBasicMaterial({ 
        color: 0x409eff, 
        transparent: true, 
        opacity: 0.3 
      })
      model.material = highlightMaterial
    }
  }

  /**
   * 删除模型
   */
  deleteModel(modelId: string): boolean {
    const model = this.models.get(modelId)
    if (!model) return false

    this.modelsGroup.remove(model)
    this.models.delete(modelId)
    
    if (model instanceof THREE.Mesh) {
      model.geometry.dispose()
      if (Array.isArray(model.material)) {
        model.material.forEach(material => material.dispose())
      } else {
        model.material.dispose()
      }
    }

    if (this.selectedModel === model) {
      this.selectedModel = null
    }

    return true
  }

  /**
   * 设置模型位置
   */
  setModelPosition(modelId: string, position: { x: number; y: number; z: number }, animate: boolean = true): void {
    const model = this.models.get(modelId)
    if (!model) return

    if (animate) {
      new TWEEN.Tween(model.position)
        .to(position, 500)
        .onUpdate(() => {
          model.position.set(position.x, position.y, position.z)
        })
        .start()
    } else {
      model.position.set(position.x, position.y, position.z)
    }
  }

  /**
   * 设置模型旋转
   */
  setModelRotation(modelId: string, rotation: { x: number; y: number; z: number }, animate: boolean = true): void {
    const model = this.models.get(modelId)
    if (!model) return

    if (animate) {
      new TWEEN.Tween(model.rotation)
        .to(rotation, 500)
        .onUpdate(() => {
          model.rotation.set(rotation.x, rotation.y, rotation.z)
        })
        .start()
    } else {
      model.rotation.set(rotation.x, rotation.y, rotation.z)
    }
  }

  /**
   * 设置模型缩放
   */
  setModelScale(modelId: string, scale: number, animate: boolean = true): void {
    const model = this.models.get(modelId)
    if (!model) return

    if (animate) {
      new TWEEN.Tween({ scale: model.scale.x })
        .to({ scale }, 500)
        .onUpdate(({ scale }) => {
          model.scale.setScalar(scale)
        })
        .start()
    } else {
      model.scale.setScalar(scale)
    }
  }

  /**
   * 重置模型变换
   */
  resetModelTransform(modelId: string): void {
    const model = this.models.get(modelId)
    if (!model) return

    const { originalPosition, originalRotation, originalScale } = model.userData
    
    this.setModelPosition(modelId, originalPosition, true)
    this.setModelRotation(modelId, originalRotation, true)
    this.setModelScale(modelId, originalScale, true)
  }

  /**
   * 获取所有模型配置
   */
  getAllModels(): ModelConfig[] {
    return Array.from(this.models.values()).map(model => this.getModelConfig(model))
  }

  /**
   * 获取模型配置
   */
  private getModelConfig(model: THREE.Object3D): ModelConfig {
    return {
      id: model.userData.id,
      name: model.userData.name,
      filePath: model.userData.filePath,
      fileType: model.userData.fileType,
      position: { 
        x: model.position.x, 
        y: model.position.y, 
        z: model.position.z 
      },
      rotation: { 
        x: model.rotation.x, 
        y: model.rotation.y, 
        z: model.rotation.z 
      },
      scale: model.scale.x,
      visible: model.visible,
      userData: model.userData
    }
  }

  /**
   * 根据名称搜索模型
   */
  searchModels(keyword: string): ModelConfig[] {
    return this.getAllModels().filter(model => 
      model.name.toLowerCase().includes(keyword.toLowerCase())
    )
  }

  /**
   * 显示/隐藏模型
   */
  setModelVisibility(modelId: string, visible: boolean): void {
    const model = this.models.get(modelId)
    if (model) {
      model.visible = visible
    }
  }

  /**
   * 获取选中的模型
   */
  getSelectedModel(): ModelConfig | null {
    return this.selectedModel ? this.getModelConfig(this.selectedModel) : null
  }

  /**
   * 清除所有模型
   */
  clearAllModels(): void {
    this.models.forEach(model => {
      this.modelsGroup.remove(model)
      if (model instanceof THREE.Mesh) {
        model.geometry.dispose()
        if (Array.isArray(model.material)) {
          model.material.forEach(material => material.dispose())
        } else {
          model.material.dispose()
        }
      }
    })
    
    this.models.clear()
    this.selectedModel = null
  }

  /**
   * 销毁管理器
   */
  dispose(): void {
    this.clearAllModels()
    this.scene.remove(this.modelsGroup)
  }
}