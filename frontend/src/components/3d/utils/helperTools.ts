import * as THREE from 'three'
import TWEEN from '@tweenjs/tween.js'
import type { HelperConfig } from './types'

export class HelperTools {
  private scene: THREE.Scene
  private gridHelper: THREE.GridHelper | null = null
  private axesHelper: THREE.AxesHelper | null = null
  private transformControls: any = null

  constructor(scene: THREE.Scene) {
    this.scene = scene
  }

  /**
   * 设置网格辅助线
   */
  setGridHelper(config: HelperConfig['gridHelper']): void {
    if (this.gridHelper) {
      this.scene.remove(this.gridHelper)
      this.gridHelper = null
    }

    if (config.enabled) {
      this.gridHelper = new THREE.GridHelper(config.size, config.divisions, config.color, config.color)
      this.scene.add(this.gridHelper)
    }
  }

  /**
   * 设置坐标轴辅助线
   */
  setAxesHelper(config: HelperConfig['axesHelper']): void {
    if (this.axesHelper) {
      this.scene.remove(this.axesHelper)
      this.axesHelper = null
    }

    if (config.enabled) {
      this.axesHelper = new THREE.AxesHelper(config.size)
      this.scene.add(this.axesHelper)
    }
  }

  /**
   * 设置变换控制器
   */
  setTransformControls(camera: THREE.Camera, renderer: THREE.WebGLRenderer, config: HelperConfig['transformControls']): void {
    if (this.transformControls) {
      this.scene.remove(this.transformControls)
      this.transformControls.dispose()
      this.transformControls = null
    }

    if (config.enabled) {
      console.warn('TransformControls 需要安装 three-transform-controls 包')
    }
  }

  /**
   * 设置模型旋转动画
   */
  rotateModel(model: THREE.Object3D, axis: 'x' | 'y' | 'z', angle: number, duration: number = 500): void {
    const currentRotation = { 
      x: model.rotation.x, 
      y: model.rotation.y, 
      z: model.rotation.z 
    }
    
    const targetRotation = { ...currentRotation }
    targetRotation[axis] += angle

    new TWEEN.Tween(currentRotation)
      .to(targetRotation, duration)
      .onUpdate(() => {
        model.rotation.set(currentRotation.x, currentRotation.y, currentRotation.z)
      })
      .start()
  }

  /**
   * 设置模型位置动画
   */
  moveModel(model: THREE.Object3D, targetPosition: { x: number; y: number; z: number }, duration: number = 500): void {
    new TWEEN.Tween(model.position)
      .to(targetPosition, duration)
      .onUpdate(() => {
        model.position.set(model.position.x, model.position.y, model.position.z)
      })
      .start()
  }

  /**
   * 重置相机位置
   */
  resetCamera(camera: THREE.Camera, target: THREE.Object3D | THREE.Vector3 = new THREE.Vector3(0, 0, 0)): void {
    if (target instanceof THREE.Object3D) {
      const box = new THREE.Box3().setFromObject(target)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())
      const maxSize = Math.max(size.x, size.y, size.z)
      
      camera.position.set(center.x, center.y + maxSize * 0.5, center.z + maxSize * 2)
      camera.lookAt(center)
    } else {
      camera.position.set(0, 2, 6)
      camera.lookAt(target)
    }
  }

  /**
   * 计算模型边界框
   */
  getModelBoundingBox(model: THREE.Object3D): { min: THREE.Vector3; max: THREE.Vector3; center: THREE.Vector3; size: THREE.Vector3 } {
    const box = new THREE.Box3().setFromObject(model)
    const center = new THREE.Vector3()
    const size = new THREE.Vector3()
    
    box.getCenter(center)
    box.getSize(size)
    
    return {
      min: box.min,
      max: box.max,
      center,
      size
    }
  }

  /**
   * 射线检测（鼠标点击选择模型）
   */
  raycastFromMouse(
    mouseEvent: MouseEvent, 
    camera: THREE.Camera, 
    renderer: THREE.WebGLRenderer, 
    objects: THREE.Object3D[]
  ): THREE.Intersection[] {
    const mouse = new THREE.Vector2()
    const rect = renderer.domElement.getBoundingClientRect()
    
    mouse.x = ((mouseEvent.clientX - rect.left) / rect.width) * 2 - 1
    mouse.y = -((mouseEvent.clientY - rect.top) / rect.height) * 2 + 1
    
    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(mouse, camera)
    
    return raycaster.intersectObjects(objects, true)
  }

  /**
   * 截图功能
   */
  takeScreenshot(renderer: THREE.WebGLRenderer, width: number = 1024, height: number = 768): string {
    const originalSize = {
      width: renderer.domElement.width,
      height: renderer.domElement.height
    }
    
    renderer.setSize(width, height, false)
    renderer.render(this.scene, this.scene.children[0] as THREE.Camera)
    
    const dataURL = renderer.domElement.toDataURL('image/png')
    
    renderer.setSize(originalSize.width, originalSize.height, false)
    
    return dataURL
  }

  /**
   * 更新动画（需要在动画循环中调用）
   */
  update(): void {
    TWEEN.update()
  }

  /**
   * 销毁所有辅助工具
   */
  dispose(): void {
    if (this.gridHelper) {
      this.scene.remove(this.gridHelper)
      this.gridHelper = null
    }
    
    if (this.axesHelper) {
      this.scene.remove(this.axesHelper)
      this.axesHelper = null
    }
    
    if (this.transformControls) {
      this.scene.remove(this.transformControls)
      this.transformControls.dispose()
      this.transformControls = null
    }
  }
}
