import * as THREE from 'three'
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js'
import type { SceneConfig } from './types'

export class BackgroundManager {
  private scene: THREE.Scene
  private currentTexture: THREE.Texture | null = null
  private currentVideoElement: HTMLVideoElement | null = null
  private currentBackgroundType: string | null = null

  constructor(scene: THREE.Scene) {
    this.scene = scene
  }

  /**
   * 设置场景背景颜色
   */
  setBackgroundColor(color: string): void {
    this.disposeCurrentResources()
    this.scene.background = new THREE.Color(color)
    this.currentBackgroundType = 'color'
  }

  /**
   * 设置场景背景图片
   */
  async setBackgroundImage(url: string, config?: { intensity?: number; 
  blurriness?: number }): Promise<void> {
    try {
      const texture = await new Promise<THREE.Texture>((resolve, 
      reject) => {
        new THREE.TextureLoader().load(url, resolve, undefined, reject)
      })
      
      this.setSceneTexture(texture, { 
        intensity: config?.intensity ?? 1, 
        blurriness: config?.blurriness ?? 0,
        type: 'image' 
      })
    } catch (error) {
      console.error('设置场景图片失败:', error)
      throw error
    }
  }

  /**
   * 设置全景图背景
   */
  async setPanoramaBackground(url: string, config?: { blurriness?: 
  number }): Promise<void> {
    try {
      const texture = await new Promise<THREE.Texture>((resolve, 
      reject) => {
        new RGBELoader().load(url, resolve, undefined, reject)
      })
      
      texture.mapping = THREE.EquirectangularReflectionMapping
      this.setSceneTexture(texture, { 
        intensity: 1, 
        blurriness: config?.blurriness ?? 0,
        isEnvironment: true,
        type: 'panorama' 
      })
    } catch (error) {
      console.error('设置全景图失败:', error)
      throw error
    }
  }

  /**
   * 设置视频背景
   */
  setVideoBackground(videoElement: HTMLVideoElement, config?: { 
  intensity?: number }): void {
    this.disposeCurrentResources()
    
    const videoTexture = new THREE.VideoTexture(videoElement)
    videoTexture.wrapS = THREE.ClampToEdgeWrapping
    videoTexture.wrapT = THREE.ClampToEdgeWrapping
    
    this.scene.background = videoTexture
    this.scene.backgroundIntensity = config?.intensity ?? 1
    
    this.currentVideoElement = videoElement
    this.currentTexture = videoTexture
    this.currentBackgroundType = 'video'
  }

  /**
   * 设置场景纹理的通用方法
   */
  private setSceneTexture(
    texture: THREE.Texture, 
    config: { intensity?: number; blurriness?: number; isEnvironment?: 
    boolean; type: string }
  ): void {
    const { intensity = 1, blurriness = 0, isEnvironment = false, 
    type } = config

    if (type !== 'video' && this.currentBackgroundType !== 'video') {
      this.disposeCurrentResources()
    }

    if (texture) {
      this.currentTexture = texture
      this.currentBackgroundType = type

      this.scene.background = texture
      this.scene.backgroundIntensity = intensity
      this.scene.backgroundBlurriness = blurriness
      
      if (isEnvironment) {
        this.scene.environment = texture
      }
    }
  }

  /**
   * 清理当前资源
   */
  private disposeCurrentResources(): void {
    if (this.currentTexture) {
      this.currentTexture.dispose()
      this.currentTexture = null
    }
    
    if (this.currentVideoElement) {
      this.currentVideoElement.pause()
      this.currentVideoElement = null
    }
    
    this.currentBackgroundType = null
    this.scene.background = null
    this.scene.environment = null
  }

  /**
   * 暂停视频播放
   */
  pauseVideo(): void {
    if (this.currentVideoElement) {
      this.currentVideoElement.pause()
    }
  }

  /**
   * 恢复视频播放
   */
  playVideo(): void {
    if (this.currentVideoElement) {
      this.currentVideoElement.play()
    }
  }

  /**
   * 获取当前背景配置
   */
  getCurrentConfig(): Partial<SceneConfig> {
    return {
      backgroundColor: this.scene.background instanceof THREE.Color 
        ? `#${this.scene.background.getHexString()}` 
        : undefined,
      backgroundIntensity: this.scene.backgroundIntensity,
      backgroundBlurriness: this.scene.backgroundBlurriness
    }
  }

  /**
   * 销毁管理器
   */
  dispose(): void {
    this.disposeCurrentResources()
  }
}
